def input_message(message: str = None, withInput: bool = True, withEnter: bool = True):
    if message is not None:
        print("[*] " % message)
    if withInput:
        input("Press enter to continue...")
    if withEnter:
        for _ in range(10):
            print()
