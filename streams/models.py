from django.db import models

class Stream(models.Model):
    # Server name (e.g., where the stream is hosted)
    server_name = models.CharField(max_length=255, blank=True, null=True)  
    
    # Stream title (optional field in case you want to add a title later)
    title = models.CharField(max_length=255, blank=True, null=True)  
    
    # Start and end times of the stream (optional, allows flexibility for not known start/end times)
    start_time = models.CharField(max_length=255, blank=True, null=True)  
    end_time = models.CharField(max_length=255, blank=True, null=True)   
    
    # Boolean to track whether the stream is live or not
    is_live = models.BooleanField(default=False)  
    
    
    def __str__(self):
        # Custom string representation of the model, useful for admin and debugging
       return (f"Server: {self.server_name}, "
            f"Title: {self.title}, "
            f"Start: {self.start_time}, "
            f"End: {self.end_time}, "
            f"Live: {self.is_live}")

