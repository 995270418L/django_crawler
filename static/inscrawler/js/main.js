$(document).ready(function(){
    $('.donate-en a').click(function(){
        var money = $('#exampleInputName2').val();
        if( !isNaN(Number(money)) && Number(money) !== 0){
            $('.donate-en a').attr('href','https://www.paypal.me/floder/' + money);
        }else{
            $('.donate-en-alert').text('please input a right number in the text area.');
            $('.donate-en-alert').removeClass('hide');
            $('.donate-en form')[0].reset();
            return false;
        }
    })
});