class Marble1D():
    """ 1d marble problem
        
        states: x, dx
        action: action [-1,1]


        |            ___                     |
        |___________|///|____G_______________|
                    <- ->
    """

    def __init__(self, goal=5, bound=[0, 10, -5, 5]):
        """ Initializes the marble game board
        
        goal (float): x position of goal where marble must within self.goal_width 
            of this goal to complete the task.
        
        bound (list): Contains bounds for marble game.
            [x lower boundary, x upper boundary, min x negative velocity, max x positive velocity]
        """
        # Number of state features
        self.n_state = 2
        
        # Number of actions. This seems to never be 
        # used and seems wrong as we have 3 actions [-1, 0, 1]???
        self.n_action = 1
        
        # Location of goal given by its x position 
        self.goal = goal
        
        # Sets boundaries for x and dx velocity 
        self.bound = bound
        
        # I think this tries to set defaults if bad input for
        # bound is given??? Can probably comment out or ignore it.
        if len(self.bound)!= 4:
             self.bound = self.bound[:2] + [-5, 5]
                
        # Creates an array where the 1st row contains min values and the 2nd row
        # contains max vaules. Not sure if min and max action matter, this
        # seems useful only for continuous actions only???
        # [[ x lower boundary, min x negative velocity, min action]
        # [x upper boundary, max x positive velocity, max action]]
        self._st_range = np.array([self.bound[:2], self.bound[2:], [-1, 1]]).T
        
        # Never used????
        self.nnNI = self.n_state + 1
        
        # Used check if marble is within a certain distance of the goal
        self.goal_width = 1
        
        # Initialize start state in case self.init isn't called
        # s[0] = x position
        # s[1] = dx or velocity in the x direction
        self._s = [0, 0]

    def init(self, start=None):
        """Initializes starting state for board      
           
           If you want to set a specific starting state or
           a random one call this funtion!
           
           Args:
               start (list): start[0] should contain the starting x 
                   position of the marble and s[1] should contain the
                   starting dx velocity. 
        """
        if start is not None:
            # Set start state to passed x and dx 
            self._s = start
        else: 
            # Randomly select start position between x bounds
            self._s = [np.random.randint(self.bound[0], self.bound[1]), 0.]
        return self._s
       
    def get_random_action(self):
        """ Randomly select a discrete action INDEX
            
            WARNING: Hardcoded for 3 actions 
        """
        return float(np.random.randint(3) -1) 

    def get_bound_act(self, a):
        """Never used???"""
        if a[0] > 1:
            return 1
        elif a[0] < -1:
            return -1
        else:
            return a[0]

    def next(self, a) :
        """ Given an action moves state s to next state s1
        
            Args:
                a (numeric): Action taken whose value can be
                    -1 for moving left, 0 for no movement, or 1
                    for moving right.
        
            Returns:
                Reward given marble is within goal location bounds
        """
        # Store curent state
        s = self._s
        
        # Not sure why this is here but if object is iterable
        # then it selects the first index.
        if isinstance(a, collections.Iterable):
            a = a[0]
            
        # Copies current state values into next state 
        # so they can be updated.
        s1 = copy(s)
        # Set velocity variable for increasing velocity over time
        dT = 0.1
        
        # Update x position
        s1[0] += dT * s[1] 
        # Update dx velocity (i.e., velocity of x)
        s1[1] += dT * (2*a - 0.2*s[1])
        
        # Adjust x velocity when hitting the bounds
        # or the sides of the case/track. Set veloctiy 
        # to 0 and set x position equal to the x bound.
        if s1[0] < self.bound[0]:
            s1[:] = [self.bound[0], 0]
        elif s1[0] > self.bound[1] :
            s1[:] = [self.bound[1], 0]

        # Clips velocity in postive and negative x direction
        s1[1] = np.clip(s1[1], self._st_range[0, 1],
                               self._st_range[1, 1])

        # Set next state equal to current state
        self._s =  s1
        
        return self.get_reward(s=s, a=a, s1=s1)

    def get_cur_state(self):
        """Returns the current state features"""
        return self._s

    def get_reward(self, s, s1, a):
        """ Returns current reward
            
            If marble's next state s1 is within a certain distance
            of the goal then a positive reward of 1 is given,
            else 0 reward is given. The distance to the goal in order 
            to recieve a positive reward is determined by self.goal_width.
        """
        return 1 if abs(s1[0] - self.goal) < self.goal_width else 0

    def get_state_range(self):
        """ Returns state min and max values
        
            This is basically the same as self.boundaries 
            but given as an NumPy array.
        """
        return self._st_range

    def get_actions(self):
        """ Return all possible actions
            
            Notes:
                move left = -1
                don't move = 0
                move right = 1
            
        """
        return np.array([-1., 0., 1.])

    def get_action_index(self, action):
        """ Returns index of a selected action
        
            Notes:
                Be aware all actions are hardcoded! 
        """
        return np.where(np.array([-1, 0, 1]) == action)[0][0]

    def draw_trajectory(self, smplX):
        """ Never used???"""
        if smplX.shape[1] == 1: return
        plt.plot(smplX[:,0],smplX[:,1])
        plt.axis([self.bound[0], self.bound[1],-5,5])
        plt.plot(smplX[0,0],smplX[0,1],'go')
        plt.plot(self.goal,0,'ro')
        # draw a goal region
        plt.fill_between([self.goal-self.goal_width, self.goal+self.goal_width],
                         [-5,-5], [5,5],
                         color="red", alpha=0.3)
        plt.xlabel("s") 
        plt.ylabel("s dot")