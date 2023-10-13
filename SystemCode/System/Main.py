import Robot
def main():
    robot = Robot()

    try:
        while True:
            robot.periodic()
    except KeyboardInterrupt as error:
        print(error)

if __name__ == "__main__":
    main()