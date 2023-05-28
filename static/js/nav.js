$(document).ready(
    function(){
        $("#ham").click(function () {
            $("#side-menu").fadeToggle();
        });

         $('#side-menu').click(function(e){
          if ($(e.target).is($(this).children())) {
        // Stop the event from bubbling up to parent elements
        e.stopPropagation();
    } else {
        $(this).hide("slow");
    }

        });
$('#bar').click(function(){
  $(".chapter").fadeToggle();

});
$('.close').click(function(){
  $(".chapter").hide("slow");

});
$(".search").click(function(){

$('#coveringss').fadeToggle();


});

$('#search-fade').click(function(){

         $("#coveringss").hide("slow");
         $('body').css({'overflow':'scroll'});
        });


  $('#bag').click(function(e){
 if ($(e.target).is($(this).children())) {
        // Stop the event from bubbling up to parent elements
        e.stopPropagation();
    } else {
        $(this).hide("slow");
    }

        });
 $("#myli").click(function () {
            $("#bag").fadeToggle();
        });

    });