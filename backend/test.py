class cube:
	c=[]
	top = ["y", "y", "y", "y", "y", "y", "y", "y", "y"]
	bottom = ["w", "w", "w", "w", "w", "w", "w", "w", "w"]
	back = ["b", "b", "b", "b", "b", "b", "b", "b", "b"]
	front = ["g", "g", "g", "g", "g", "g", "g", "g", "g"]
	left = ["r", "r", "r", "r", "r", "r", "r", "r", "r"]
	right = ["o", "o", "o", "o", "o", "o", "o", "o", "o"]
    def __init__(self):
    	self.top = ["y", "y", "y", "y", "y", "y", "y", "y", "y"]
        self.bottom = ["w", "w", "w", "w", "w", "w", "w", "w", "w"]
        self.back = ["b", "b", "b", "b", "b", "b", "b", "b", "b"]
        self.front = ["g", "g", "g", "g", "g", "g", "g", "g", "g"]
        self.left = ["r", "r", "r", "r", "r", "r", "r", "r", "r"]
        self.right = ["o", "o", "o", "o", "o", "o", "o", "o", "o"]
        self.c = [cube.top, cube.bottom, cube.left, cube.right, cube.front, cube.back]
    def gettop(self):
        top=1
        return self.top 
        #returns the arraylist instead of 1 because top is a local variable inside the method whereas self.top    returns the global variable inside the class
    
	def u(self):
        top=self.c[0]
        left=self.c[2]
        right=self.c[3]
        front=self.c[4]
        back=self.c[5]
        new_top = [top[6], top[3], top[0], top[7], top[4], top[1], top[8], top[5], top[2]]
        new_front = [right[0], right[1], right[2], front[3], front[4], front[5], front[6], front[7], front[8]]
        new_right = [back[0], back[1], back[2], right[3], right[4], right[5], right[6], right[7], right[8]]
        new_back = [left[0], left[1], left[2], back[3], back[4], back[5], back[6], back[7], back[8]]
        new_left = [front[0], front[1], front[2], left[3], left[4], left[5],left[6], left[7], left[8]]
        self.c[0]=new_top
        self.c[2]=new_left
        self.c[3]=new_right
        self.c[4]=new_front
        self.c[5]=new_back
        return 'U'
        
def main():
    moveList=[]
    cube1 = cube()
    moveList.append(cube1.u())
    return moveList
    
main()