class RobotController(object):
    def __init__(self):
        self.robotStates = []

    def moveDemo(self, motionTime):
        stopTime = datetime.datetime.now() + datetime.timedelta(0,motionTime)
        while datetime.datetime.now() < stopTime:
            print("Robot is moving...")
            time.sleep(1)
        print("Robot stopped")
        return 0

    def doCallback(self, callback):
        print("server: doing callback 1 to client")
        try:
            callback.call1()
        except:
            print("got an exception from the callback.")
            print("".join(Pyro4.util.getPyroTraceback()))
        print("server: doing callback 2 to client")
        try:
            callback.call2()
        except:
            print("got an exception from the callback.")
            print("".join(Pyro4.util.getPyroTraceback()))
        print("server: callbacks done")



if __name__ == '__main__':
    robotController = RobotController()
    if os.name == 'posix':
        daemon = Pyro4.Daemon(host="192.168.1.104", port=8000); 
    else:
        daemon = Pyro4.Daemon(host="localhost", port=8000);
    Pyro4.Daemon.serveSimple(
    { robotController: "robotController"},
    ns=False,
    daemon=daemon,
    verbose = True
    )