from djangorestframework.resources import ModelResource

class AuthModelResource(ModelResource):

  
    def __init__(self, view):
        super(ModelResource, self).__init__(view)
        self.current_user = view.user;
        
