from math                           import pi, sin, cos

# i will be using panda3d to make the game
from direct.showbase.ShowBase       import ShowBase
from direct.task                    import Task
from direct.actor.Actor             import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core                   import Point3

# this is the main class
# it inherits from ShowBase, which loads the majority of panda3d
# it also causes the window to appear
class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # disabling the default camera controls
        self.disableMouse()

        # using loadModel to load a static model
        self.scene = self.loader.loadModel("models/environment")

        # there is a data structure called Scene Graph which contains all the objects that get rendered
        # by giving the model a parent, it gets installed in the Scene Graph
        self.scene.reparentTo(self.render)

        # shrinking the model in x, y and z by a quarter
        self.scene.setScale(0.25, 0.25, 0.25)

        # the coordinates are the position in x and y and the height
        self.scene.setPos(-8, 42, 0)
        
        # add our task to the task manager
        # it means that the task gets called every frame
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # loading the panda actor
        # use Actor to load animated models
        self.panda_actor = Actor("models/panda-model",              # file containing the model
                                 {"walk": "models/panda-walk4"})    # python dict containing the names of the animation files
        self.panda_actor.setScale(0.005, 0.005, 0.005)
        self.panda_actor.reparentTo(self.render)

        # loop the animation
        self.panda_actor.loop("walk")

        # creating the 4 intervals for the panda to walk back and forth
        # a posInterval gradually adjusts the position of a model from one position to another in the given time
        pos_interval_1  = self.panda_actor.posInterval(13,                          # 13 seconds
                                                       Point3(0, -10, 0),
                                                       startPos = Point3(0, 10, 0))
        pos_interval_2  = self.panda_actor.posInterval(13,
                                                       Point3(0, 10, 0),
                                                       startPos = Point3(0, -10, 0))

        # similarly, a hprInterval rotates the model in the given time
        hpr_interval_1  = self.panda_actor.hprInterval(3,                           # 3 seconds
                                                       Point3(180, 0, 0),
                                                       startHpr = Point3(0, 0, 0))
        hpr_interval_2  = self.panda_actor.hprInterval(3,
                                                       Point3(0, 0, 0),
                                                       startHpr = Point3(180, 0, 0))

        # creating and playing the sequence that coordinates the intervals
        self.panda_pace = Sequence(pos_interval_1, hpr_interval_1,
                                   pos_interval_2, hpr_interval_2,
                                   name = "panda_pace")
        self.panda_pace.loop()

    def spinCameraTask(self, task):

        # the desired position calculated based on the time that has elapsed (6 degrees per second)
        angle_degrees   = task.time * 6.0
        angle_radians   = angle_degrees * (pi / 180.0)

        # x and y move while z (aka height) stays fixed at 3
        self.camera.setPos(20 * sin(angle_radians), -20 * cos(angle_radians), 3)

        # the setHpr actually sets the orientation
        self.camera.setHpr(angle_degrees, 0, 0)

        # as long as this gets returned, the task will be called in the next frame
        return Task.cont

app = MyApp()
app.run()
