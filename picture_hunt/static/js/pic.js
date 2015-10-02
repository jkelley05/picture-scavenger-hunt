$(document).ready(function()
{

    $(document).delegate('button.delete', 'click', function(event)
    {
        del = confirm("Are you sure you want to delete this?");
        
        if( !del )
        {
            event.preventDefault();
        }

    });

});
