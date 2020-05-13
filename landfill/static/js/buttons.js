$(document).ready(
    function(){
        $("#barcode").focus()
        $('.fa-arrow-up').click(
            function(){
                var curVal = Number($(this).next().val())
                if (!isNaN(curVal) && curVal > 0) {
                    $(this).next().val(curVal += 1)
                } else {
                    $(this).next().val(1)
                }
            }
        )
        $('.fa-arrow-down').click(
            function(){
                var curVal = Number($(this).prev().val())
                if (!isNaN(curVal) && curVal > 1) {
                    $(this).prev().val(curVal - 1)
                } else {
                    $(this).prev().val("")
                }
            }
        )
    }
)