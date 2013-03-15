# `django-changes`

A utility to store and access information about changes on objects in a Django
project.


## Installation

Add to your Python path or `setup.py install` and add `'changes'` to your
`INSTALLED_APPS` setting.


## Usage

You can use by importing the helper:

    from changes import changes
    # ...
    changes.add_change(someobj, who=request.user)

Or by using the object directly:

    from changes.models import Change
    # ...
    Change.objects.add_change_for_object(someobj, why='Because')


To get a queryset of changes that were added for an objects:

    changes.get_changes_for(someobj)

or:

    Change.objects.get_changes_for_object(someobj)


To get a queryset of changes that were made by a user:

    changes.get_changes_by(someuser)

or:

    Change.objects.get_changes_by_user(someuser)


You can also do things like this:

    Change.objects.all().by_user(someuser)
    changes.get_changes_for(someobj).anonymous()


See the source code for more.


# Need Help?

Email: rvause@gmail.com

Twitter: http://twitter.com/rvause
