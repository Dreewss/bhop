import pymem
import win32api
import time

# Offsets 
LOCAL_PLAYER = 0xDB458C  
FORCE_JUMP = 0x527998C   
HEALTH = 0x100            
FLAGS = 0x104            

def bhop() -> None:
    try:
        pm = pymem.Pymem('cs2.exe')
    except pymem.exception.ProcessNotFound:
        print("CS2 not running. Please start the game first.")
        return

    # Get module address
    client = None
    for module in list(pm.list_modules()):
        if module.name.lower() == 'client.dll':
            client = module.lpBaseOfDll
            break
    
    if not client:
        print("Failed to find client.dll")
        return

    print("Bunny hop script started. Press SPACE to bhop...")

    # Hack loop
    while True:
        time.sleep(0.01)
        
        
        if not win32api.GetAsyncKeyState(0x20):
            continue

        try:
            local_player_addr = pm.read_uint(client + LOCAL_PLAYER)
            
            if not local_player_addr:
                continue

            # Check if alive
            player_health = pm.read_uint(local_player_addr + HEALTH)
            if not player_health:
                continue
            
            # Check if on ground
            player_flags = pm.read_uint(local_player_addr + FLAGS)
            if player_flags & (1 << 0): 
                pm.write_uint(client + FORCE_JUMP, 6)  # Jump
                time.sleep(0.01)
                pm.write_uint(client + FORCE_JUMP, 4)  # Release
                
        except pymem.exception.MemoryReadError:
            continue
        except pymem.exception.MemoryWriteError:
            continue
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == '__main__':
    bhop()
