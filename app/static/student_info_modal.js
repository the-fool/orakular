$(document).ready(function() {
    $('tr.student-info').click(function() {
	var id=$(this).data('id');
	var name=$(this).children().eq(1).text();
	console.log(name);
	$('#student_info').data('id', id);
	$('#student_info .modal-title').text(name);
	$('#student_info .modal-body').load('/ajax/student_modal?sid='+id, function() {
	  /*  $('ul.nav-pills li a').click(function () 
	     {
		 var id=$(this).attr('href');
	
		 $('ul.nav-pills li.active').removeClass('active');
		 $(this).parent('li').addClass('active');
		 
	//	$(this).tab('show');
	     });*/
	  
	});
	$('#student_info').modal('show');
    });
});
