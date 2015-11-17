$(document).ready(function() {
    $('fname').each(function() {
	var id = $(this).data('id');
	var name = $(this).text();
	$('td.fid-'+id).text(name);
    });
});
