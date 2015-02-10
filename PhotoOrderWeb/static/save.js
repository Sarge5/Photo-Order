$(document).ready(function(){
    $(".order").change(function(){
        idphoto = $(this).parent().prop("id")
        ordered = $(this).prop("checked")
        $.ajax({
            url: "/order",
            type: "POST",
            data: {
                idphoto: idphoto,
                ordered: ordered
            },
            success: function(response){
                console.log(response)
            },
            error: function(response){
                console.log(response)
            }
        })
    })
})