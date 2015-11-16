$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    $(".nav-tabs li").first().addClass("active");
    $(".tab-pane").first().addClass("in active");
    $(".edit-grade").editable({
	validate: function(value) {
	    if($.trim(value) == '') {
		return 'This field is required';
	    }
	    if($.isNumeric(value)) {
		if (value > 100 || value < 0) {
		    return 'Must be between 0 and 100';
		}
	    }
	    else {
		return 'Must enter a number';
	    }
	}
    });
});
