class Fustrum :
    def __init__(self,r,parent):
        self.rayon = r
        self.parent = parent
        self.perceptionList = []

    def inside(self,obj):
        if hasattr(obj, "position"):
            if obj.position.distance_to(self.parent.position) < self.rayon:
                return True
        return False