$(document).ready(function () {

    $('#informationBlock').hide();

    $('#slideToggle').on('click', function (){

        $('#informationBlock').slideToggle(1000);

        $(this).css("background","#273959");

    });

});
