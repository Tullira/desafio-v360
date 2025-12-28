def ask_running_option():
    option = int(input("Qual tipo de execução você deseja?\n1 - Headed\n2 - Headless\n"))
    while (option != 1 and option != 2):
        print("Opção inválida")
        option = int(input("Qual tipo de execução você deseja?\n1 - Headed\n2 - Headless\n"))

    if option == 1:
        runOption = False
    else:
        runOption = False
        
    return runOption