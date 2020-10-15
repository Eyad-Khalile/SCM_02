// make the Email in the form register required filde
// let astr = '<span class="asteriskField">*</span>';
// $('input.emailinput').parent().prev('label').addClass('requiredField').append(astr);

$("form.form-signin").find('label[for="id_username"]').addClass("d-none");
$("form.form-signin").find("#id_username").attr("placeholder", "اسم المستخدم");

$("form.form-signin").find('label[for="id_password"]').addClass("d-none");
$("form.form-signin").find("#id_password").attr("placeholder", "كلمة المرور");

// ORG PROFILE
$("#div_id_city_work").hide();
if ($("#id_position_work").val() == "SY") {
    $("#div_id_city_work").show();
}
$("#id_position_work").change(function () {
    let country = $("#id_position_work").val();
    switch (country) {
        case "SY":
            $("#div_id_city_work").show();
            break;

        default:
            $("#div_id_city_work").hide();
            break;
    }
});

$("#div_id_org_registered_country").hide();
if ($("#id_is_org_registered").val() == "1") {
    $("#div_id_org_registered_country").show();
}
$("#id_is_org_registered").change(function () {
    let org_reg = $("#id_is_org_registered").val();
    switch (org_reg) {
        case "1":
            $("#div_id_org_registered_country").show();
            break;
        default:
            $("#div_id_org_registered_country").hide();
            break;
    }
});

// INPUT ACCEPT YEAR ONLY
$(
    "input#id_start_date,  input#id_end_date, input#id_date_of_establishment"
).attr({
    maxlength: "4",
    spellcheck: "false",
    oninput: "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\\..*)\\./g, '$1').replace(/^(0*)/,'');",
    placeholder: "Ex : YYYY",
});

$('input#id_start_date_pub, input#id_end_date_pub').attr('type', 'date');

// FIELD PHONE
$("#id_phone").attr({
    maxlength: "16",
    oninput: "this.value = this.value.replace(/[^0-9+]/g, '');",
    placeholder: "Ex : 00963 / +963",
});

// LES CHARACTERS SPECIAUX
$(
    "#id_name, #id_name_en_ku, #id_short_cut, #id_message, #id_name_managing_director, #id_name_ceo, #id_name_person_contact, #id_org_adress, #id_coalition_name"
).attr({
    minlength: "3",
    oninput: "this.value = this.value.replace(/[^a-zA-Z0-9 ]/gi, '');",
});

// MEMBERS COUNT
$("#id_org_members_count, #id_org_members_womans_count").attr({
    maxlength: "3",
    oninput: "this.value = this.value.replace(/[^0-9.]/g, '');",
    placeholder: "Ex : 1 - 900",
});

$("#div_id_coalition_name").hide();
if ($("#id_org_member_with").val() == "1") {
    $("#div_id_coalition_name").show();
}

$("#id_org_member_with").change(function () {
    let mem = $("#id_org_member_with").val();
    switch (mem) {
        case "":
            $("#div_id_coalition_name").hide();
            break;
        case "0":
            $("#div_id_coalition_name").hide();
            break;
        case "1":
            $("#div_id_coalition_name").show();
            break;
    }
});

// ACCEPT ORG
$("form.confirm").find("#id_publish").hide();
$("form.confirm").submit(function () {
    $("form.confirm").find("#id_publish").attr("checked", true);
});

// REFIOUSE ORG
$("form.deconfirm").find("#id_publish").hide();
$("form.deconfirm").submit(function () {
    $("form.deconfirm").find("#id_publish").attr("checked", false);
});



// URL
var pathname = window.location.pathname; // Returns path only (/path/example.html)
// var url = window.location.href;     // Returns full URL (https://example.com/path/example.html)
var origin = window.location.origin; // Returns base URL (https://example.com)

// console.log('olde path : ' + pathname);
// console.log(url);
// console.log(origin);
// console.log(location);


function removeCharacter(str) {
    let tmp = str.split("");
    return tmp.slice(3).join("");
}


// if (pathname[1] == "e" && pathname[2] == "n") {
//     let output = removeCharacter(pathname);
//     console.log(`Output is ${output}`);
// }

// LANGE SWICHER
$("#chnage-lange").change(function () {
    let lan_sel = $("#chnage-lange").val();
    switch (lan_sel) {
        case "ar":
            document.location.href = origin + removeCharacter(pathname);
            break;
        case "en":
            document.location.href = origin + "/en" + pathname;
            break;
    }









});