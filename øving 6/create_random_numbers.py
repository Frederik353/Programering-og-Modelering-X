import random
import os




def random_function():
    return  random.randint(0, upper)

def main():
    writepath = "./random.txt"
    # mode = "a" if os.path.exists(writepath) else "w"
    mode = "w"
    with open(writepath, mode) as f:
        # f.write("\n")
        for i in range(1000):
            temp = random.randint(0,i)
            if temp % 19 == 0:
                temp = -temp
            if temp % 37 == 0: # bruker ny if siden 37 * 19 er 703 som er innenfor mengden vi bruker
                temp = temp // 3
            f.write(str(temp) + "\n")


if __name__ == "__main__":
    main()
