from kivy.clock import Clock

class C(object):    
    def write(self):
        print ('Hello world')
        
class myclock(object):
    def my_callback(dt):
        pass
    def mycall(self, dt):
       Clock.schedule_once(self.my_callback, dt) 

class Foo(object):
    def start(self):
        Clock.schedule_interval(self.callback, 0)

    def callback(self, dt):
        print('In callback')



x = C()
x.write()

# So you should do the following and keep a reference to the instance
# of foo until you don't need it anymore!
foo = Foo()
foo.start()
y = C()
y.write()

import asynckivy as ak

async def some_task():
    # wait for 1sec
    dt = await ak.sleep(1)
    print(f'{dt} seconds have passed')



    # nest as you want.
    # wait for a button to be pressed AND (5sec OR 'other_async_func' to complete)
    tasks = await ak.and_(
        ak.event(button, 'on_press'),
        ak.or_(
            ak.sleep(5),
            other_async_func(),
        ),
    )
    child_tasks = tasks[1].result
    print("5sec passed" if child_tasks[0].done else "other_async_func has completed")

ak.start(some_task())