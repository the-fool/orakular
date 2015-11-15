$(document).ready(function() {
    $('tr.student-info').click(function() {
	var id=$(this).data('id');
	var name=$(this).children().eq(1).text();
	console.log(name);
	$('#student_info').data('id', id);
	$('#student_info .modal-title').text(name);
	$('#student_info .modal-body').load('/ajax/student_modal?sid='+id, function() {
	    $('ul.nav-pills li a').click(function () 
	     {
		 var id=$(this).data('id');
	
		 $('ul.nav-pills li.active').removeClass('active');
		 $(this).parent('li').addClass('active');

		 $('.tab-content div.active').toggle()
		     .removeClass('active').css("opacity", "0");
		 $('#'+id).addClass('active').toggle().css("opacity", "100");
	     });
	});
	$('#student_info').modal('show');
    });
});
