// make the Email in the form register required filde
// let astr = '<span class="asteriskField">*</span>';
// $('input.emailinput').parent().prev('label').addClass('requiredField').append(astr);

$('form.form-signin').find('label[for="id_username"]').addClass('d-none');
$('form.form-signin').find('#id_username').attr('placeholder', 'اسم المستخدم');

$('form.form-signin').find('label[for="id_password"]').addClass('d-none');
$('form.form-signin').find('#id_password').attr('placeholder', 'كلمة المرور');




// ORG PROFILE
$('#div_id_city_work').hide();
if ($('#id_position_work').val() == 'SY') {
    $('#div_id_city_work').show();
}
$('#id_position_work').change(function () {
    let country = $('#id_position_work').val();
    switch (country) {
        case 'SY':
            $('#div_id_city_work').show();
            break;

        default:
            $('#div_id_city_work').hide();
            break;
    }
});

$('#div_id_org_registered_country').hide();
if ($('#id_is_org_registered').val() == '1') {
    $('#div_id_org_registered_country').show();
}
$('#id_is_org_registered').change(function () {
    let org_reg = $('#id_is_org_registered').val();
    switch (org_reg) {
        case '1':
            $('#div_id_org_registered_country').show();
            break;
        default:
            $('#div_id_org_registered_country').hide();
            break;
    }
});