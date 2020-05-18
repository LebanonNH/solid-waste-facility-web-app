$(document).ready(
    function(){
        $("#barcode").focus()
        $('.fa-plus').click(
            function(){
                var curVal = Number($(this).prev().val())
                if (!isNaN(curVal) && curVal > 0) {
                    $(this).prev().val(curVal += 1)
                } else {
                    $(this).prev().val(1)
                }
            }
        )
        $('.fa-minus').click(
            function(){
                var curVal = Number($(this).next().val())
                if (!isNaN(curVal) && curVal > 1) {
                    $(this).next().val(curVal - 1)
                } else {
                    $(this).next().val("")
                }
            }
        )
    }
)