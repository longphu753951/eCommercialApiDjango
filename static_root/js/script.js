$(document).ready(function(){
    $('#id_color').change(function() {
        console.log('asdasdasd')
    })
    $('#id_product').on('change', function() {
        console.log($('#id_product option:selected').text())
    })
})