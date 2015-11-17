$(document).ready(function() {
 
    $('.fname').each(function() {
	var id = $(this).data('id');
	var name = $(this).text();
	 $('.fid-'+id).each(function() {
	     $(this).text(name)
	 });
    });
   
});
