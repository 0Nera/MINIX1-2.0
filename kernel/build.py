import os, shutil, sys, tarfile, time


CC = "i686-elf-gcc -g -w -ffreestanding -I kernel/include/ -c"


def build_kernel():
    start_time = time.time()
    print("Building kernel")

    SRC_TARGETS = []
    BIN_TARGETS = []

    for path, directories, files in os.walk(".\\"):
        for i in files:
            if i.endswith('.c'):
                SRC_TARGETS.append(os.path.join(path, i))
                BIN_TARGETS.append(os.path.join("bin\\", os.path.splitext(i)[0]+'.o'  ))
            #elif i.endswith('.s'):
            #    SRC_TARGETS.append(os.path.join(path, i))
            #   BIN_TARGETS.append(os.path.join("bin\\", os.path.splitext(i)[0]+'_ASM.o'  ))

    shutil.rmtree("bin/", ignore_errors=True)
    os.mkdir("bin/")
    
    for i in range(0, len(SRC_TARGETS)):
        os.system(f"{CC} {SRC_TARGETS[i]} -o {BIN_TARGETS[i]}")
        

    # Получаем список файлов в переменную files
    files = os.listdir("bin/")

    # Фильтруем список
    bins = filter(lambda x: x.endswith('.o'), files)
    OBJ = ""
    
    for i in bins:
        OBJ += f"bin/{i} "

    print(f"Build end at: {time.time() - start_time}")


def create_iso():
    print("Creating ISO")
    start_time = time.time()

    if sys.platform == "linux" or sys.platform == "linux2":
        os.system("grub-mkrescue -o \"Minix.iso\" isodir/ -V Minix")
    else:
        os.system("ubuntu run grub-mkrescue -o \"Minix.iso\" isodir/ -V Minix ")
    
    print(f"Build end at: {time.time() - start_time}")


def run_qemu():
    if os.path.exists("ata.vhd"):
        pass
    else:
        os.system("qemu-img create -f raw ata.vhd 32M")
    
    qemu_command = "qemu-system-i386 -name Minix -soundhw all -m 16" \
        " -netdev socket,id=n0,listen=:2030 -device rtl8139,netdev=n0,mac=11:11:11:11:11:11 " \
        " -cdrom Minix.iso -hda ata.vhd -serial  file:Qemu.log"
        
    os.system(
        qemu_command
        )


if __name__ == "__main__":
    try:
        start_time = time.time()

        # Стандартная сборка
        
        if len(sys.argv) == 1:
            build_kernel()
            create_iso()
            run_qemu()
        else:
            for i in range(1, len(sys.argv)):
                if sys.argv[i] == "kernel":
                    build_kernel()
                elif sys.argv[i] == "iso":
                    create_iso()
                elif sys.argv[i] == "run":
                    run_qemu()
                else:
                    print(f"Ошибка, неизвестный аргумент: {sys.argv[i]}")
        print(f"Конец: {time.time() - start_time}")

    except Exception as E:
        print(E)