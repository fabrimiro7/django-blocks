from django.db import models


class AppConfigurator(models.Model):
    """
    Model representing an application configurator.

    Attributes:
        name (str): The name of the application.
        enabled (bool): Indicates whether the application is enabled.
        modules_dependencies (ManyToManyField): Dependencies of the application.
    """
    name = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=False)
    modules_dependencies = models.ManyToManyField('self', blank=True)

    def __str__(self):
        """
        Returns the string representation of the AppConfigurator instance.

        Returns:
            str: The name of the application.
        """
        return self.name

    def enable_dependencies(self):
        """
        Enables all dependencies of the AppConfigurator instance if it is enabled.
        This method is called recursively to ensure all nested dependencies are enabled.
        """
        if self.enabled:
            for dependency in self.modules_dependencies.all():
                if not dependency.enabled:
                    dependency.enabled = True
                    dependency.save()
                    dependency.enable_dependencies()  # Recursively enable dependencies

    def save(self, *args, **kwargs):
        """
        Overrides the save method to enable dependencies if the instance is enabled.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().save(*args, **kwargs)
        if self.enabled:
            self.enable_dependencies()

    class Meta:
        """
        Meta options for the AppConfigurator model.
        """
        ordering = ['name']