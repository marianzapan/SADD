//CLOSE NOTIFICATION
document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
        const $notification = $delete.parentNode;
        $delete.addEventListener('click', () => {
            $notification.parentNode.removeChild($notification);
            if (url.includes('?forbidden=')) window.location.replace(url.substring(0, url.lastIndexOf('?forbidden=')))
        });
    });
});

//MOSTRAR FILE NAMES
const fileInputXML = document.querySelector('#xml input[type=file]');
if (fileInputXML != null) {
   fileInputXML.onchange = () => {
    if (fileInputXML.files.length > 0) {
      const fileNameXML = document.querySelector('#xml .file-name');
      fileNameXML.textContent = fileInputXML.files[0].name;
    }
  } 
}
const fileInputPDF = document.querySelector('#pdf input[type=file]');
if (fileInputPDF != null) {
    fileInputPDF.onchange = () => {
        if (fileInputPDF.files.length > 0) {
            const fileNamePDF = document.querySelector('#pdf .file-name');
            fileNamePDF.textContent = fileInputPDF.files[0].name;
        }
    }   
}
const fileInputDoc = document.querySelector('#doc input[type=file]');
if (fileInputDoc != null) {
    fileInputDoc.onchange = () => {
        if (fileInputDoc.files.length > 0) {
            const fileNameDoc = document.querySelector('#doc .file-name');
            fileNameDoc.textContent = fileInputDoc.files[0].name;
        }
    }   
}
const fileInputImg = document.querySelector('#img input[type=file]');
if (fileInputImg != null) {
    fileInputImg.onchange = () => {
        if (fileInputImg.files.length > 0) {
            const fileNameImg = document.querySelector('#img .file-name');
            fileNameImg.textContent = fileInputImg.files[0].name;
        }
    }   
}
const fileInput = document.querySelector('.modal#cambiar input[type=file]');
if (fileInput != null) {
    fileInput.onchange = () => {
        if (fileInput.files.length > 0) {
            const fileName = document.querySelector('.file-name');
            fileName.textContent = fileInput.files[0].name;
        }
    }   
}

//BUSCAR SELECT
function buscarConc(indice1, indice2, indice3, indice4, indice5) {
    var input, filtro, cont, tarjeta, campo1, campo2, campo3, campo4, campo5, i, txt1, txt2, txt3, txt4, txt5;
    input = document.getElementById("busqueda");
    filtro = input.value.toUpperCase();
    cont = document.getElementById("cont-tarjetas");
    tarjeta = cont.getElementsByClassName("tarjeta-lg");

    for (i = 0; i < tarjeta.length; i++) {
        campo1 = tarjeta[i].getElementsByTagName("p")[indice1];
        campo2 = tarjeta[i].getElementsByTagName("p")[indice2];
        campo3 = tarjeta[i].getElementsByTagName("p")[indice3];
        campo4 = tarjeta[i].getElementsByTagName("p")[indice4];
        campo5 = tarjeta[i].getElementsByTagName("p")[indice5];
        
        if (campo1 || campo2 || campo3 || campo4 || campo5) {
            txt1 = campo1.textContent || campo1.innerText;
            txt2 = campo2.textContent || campo2.innerText;
            txt3 = campo3.textContent || campo3.innerText;
            txt4 = campo4.textContent || campo4.innerText;
            txt5 = campo5.textContent || campo5.innerText;
            if (txt1.toUpperCase().indexOf(filtro) > -1 || txt2.toUpperCase().indexOf(filtro) > -1 || txt3.toUpperCase().indexOf(filtro) > -1
            || txt4.toUpperCase().indexOf(filtro) > -1 || txt5.toUpperCase().indexOf(filtro) > -1) {
                tarjeta[i].style.display = "";
            } else {
                tarjeta[i].style.display = "none";
            }
        }
    }
}
function buscarConc(indice1, indice2, indice3, indice4) {
    var input, filtro, cont, tarjeta, campo1, campo2, campo3, campo4, i, txt1, txt2, txt3, txt4;
    input = document.getElementById("busqueda");
    filtro = input.value.toUpperCase();
    cont = document.getElementById("cont-tarjetas");
    tarjeta = cont.getElementsByClassName("tarjeta-lg");

    for (i = 0; i < tarjeta.length; i++) {
        campo1 = tarjeta[i].getElementsByTagName("p")[indice1];
        campo2 = tarjeta[i].getElementsByTagName("p")[indice2];
        campo3 = tarjeta[i].getElementsByTagName("p")[indice3];
        campo4 = tarjeta[i].getElementsByTagName("p")[indice4];
        
        if (campo1 || campo2 || campo3 || campo4) {
            txt1 = campo1.textContent || campo1.innerText;
            txt2 = campo2.textContent || campo2.innerText;
            txt3 = campo3.textContent || campo3.innerText;
            txt4 = campo4.textContent || campo4.innerText;
            if (txt1.toUpperCase().indexOf(filtro) > -1 || txt2.toUpperCase().indexOf(filtro) > -1 || txt3.toUpperCase().indexOf(filtro) > -1
            || txt4.toUpperCase().indexOf(filtro) > -1) {
                tarjeta[i].style.display = "";
            } else {
                tarjeta[i].style.display = "none";
            }
        }
    }
}
function buscarConc(indice1, indice2, indice3) {
    var input, filtro, cont, tarjeta, campo1, campo2, campo3, i, txt1, txt2, txt3;
    input = document.getElementById("busqueda");
    filtro = input.value.toUpperCase();
    cont = document.getElementById("cont-tarjetas");
    tarjeta = cont.getElementsByClassName("tarjeta-lg");

    for (i = 0; i < tarjeta.length; i++) {
        campo1 = tarjeta[i].getElementsByTagName("p")[indice1];
        campo2 = tarjeta[i].getElementsByTagName("p")[indice2];
        campo3 = tarjeta[i].getElementsByTagName("p")[indice3];
        
        if (campo1 || campo2 || campo3) {
            txt1 = campo1.textContent || campo1.innerText;
            txt2 = campo2.textContent || campo2.innerText;
            txt3 = campo3.textContent || campo3.innerText;
            if (txt1.toUpperCase().indexOf(filtro) > -1 || txt2.toUpperCase().indexOf(filtro) > -1 || txt3.toUpperCase().indexOf(filtro) > -1) {
                tarjeta[i].style.display = "";
            } else {
                tarjeta[i].style.display = "none";
            }
        }
    }
}

//VALIDACIÓN RFC
var rfc = document.getElementById("rfc");
if (rfc != null){
    rfc.addEventListener("keyup", () => {
    rfc.value = rfc.value.toUpperCase();
    console.log(rfc.value)
    if (rfc.validity.patternMismatch) rfc.setCustomValidity("Se espera un RFC válido.");
    else rfc.setCustomValidity("");
    }); 
}

//MOSTRAR CONTRASEÑA
$('#eyePassword').click(function() {
    if ($('#password').attr("style") == '-webkit-text-security: disc !important')
        $('#password').attr("style", '-webkit-text-security: none !important')
    else $('#password').attr("style", '-webkit-text-security: disc !important')
});

//LOGICA CHECKBOXES
$('#fp_u').on('click', toggleFP); $('#fp_d').on('click', toggleFP);
$('#fc_u').on('click', toggleFC); $('#fc_d').on('click', toggleFC);
$('#p_u').on('click', toggleP); $('#p_d').on('click', toggleP);
$('#pl_u').on('click', togglePL); $('#pl_d').on('click', togglePL);
$('#c_u').on('click', toggleC); $('#c_d').on('click', toggleC);
$('#a_u').on('click', toggleA); $('#a_d').on('click', toggleA);
$('#u_u').on('click', toggleU); $('#u_d').on('click', toggleU); $('#u_c').on('click', toggleU);

function toggleFP() {
    if ($('#fp_u').is(':checked') || $('#fp_d').is(':checked')) { $("#fp_r").prop('disabled', true); $("#fp_r").prop('checked', true); }
    else { $("#fp_r").prop('disabled', false); $("#fp_r").prop('checked', false); }     
}
function toggleFC() {
    if ($('#fc_u').is(':checked') || $('#fc_d').is(':checked')) { $("#fc_r").prop('disabled', true); $("#fc_r").prop('checked', true); }
    else { $("#fc_r").prop('disabled', false); $("#fc_r").prop('checked', false); } 
}
function toggleP() {
    if ($('#p_u').is(':checked') || $('#p_d').is(':checked')) { $("#p_r").prop('disabled', true); $("#p_r").prop('checked', true); }
    else { $("#p_r").prop('disabled', false); $("#p_r").prop('checked', false); } 
}
function togglePL() {
    if ($('#pl_u').is(':checked') || $('#pl_d').is(':checked')) { $("#pl_r").prop('disabled', true); $("#pl_r").prop('checked', true); }
    else { $("#pl_r").prop('disabled', false); $("#pl_r").prop('checked', false); } 
}
function toggleC() {
    if ($('#c_u').is(':checked') || $('#c_d').is(':checked')) { $("#c_r").prop('disabled', true); $("#c_r").prop('checked', true); }
    else { $("#c_r").prop('disabled', false); $("#c_r").prop('checked', false); } 
}
function toggleA() {
    if ($('#a_u').is(':checked') || $('#a_d').is(':checked')) { $("#a_r").prop('disabled', true); $("#a_r").prop('checked', true); }
    else { $("#a_r").prop('disabled', false); $("#a_r").prop('checked', false); } 
}
function toggleU() {
    if ($('#u_u').is(':checked') || $('#u_d').is(':checked') || $('#u_c').is(':checked')) { $("#u_r").prop('disabled', true); $("#u_r").prop('checked', true); }
    else { $("#u_r").prop('disabled', false); $("#u_r").prop('checked', false); } 
}

//FILTRO DROPDOWN
$(document).ready(function () {
    $('.selectize').selectize({
        sortField: 'text'
    });
 });

//FECHA DE VENCIMIENTO TOGGLE
$('#si_ampara').click(function() {
    $('#vencimiento').slideDown();
    document.querySelector('#vencimiento input').required = true
});
$('#no_ampara').click(function() {
    $('#vencimiento').slideUp();
    document.querySelector('#vencimiento input').required = false
});

if ($('#vencimiento input').val() != undefined && $('#vencimiento input').val().length != 0){
    $('#no_ampara').prop('checked', false);
    $('#si_ampara').prop('checked', true);
    $('#vencimiento').show();
    document.querySelector('#vencimiento input').required = true;
    if ($('#no_ampara').click(function() {
        $('#vencimiento').hide();
        $('#vencimiento input').removeAttr('value');
        document.querySelector('#vencimiento input').required = false;
    }));
}

//AGREGAR DOCUMENTO TOGGLE
$('#si_doc').click(function() {
    $('.docs').slideDown(300);
    if (document.querySelector('#xml input') != null) document.querySelector('#xml input').required = true
    if (document.querySelector('#pdf input') != null) document.querySelector('#pdf input').required = true
    if (document.querySelector('#doc input') != null) document.querySelector('#doc input').required = true
});
$('#no_doc').click(function() {
    $('.docs').slideUp(300);
    if (document.querySelector('#xml input') != null) document.querySelector('#xml input').required = false
    if (document.querySelector('#pdf input') != null) document.querySelector('#pdf input').required = false
    if (document.querySelector('#doc input') != null) document.querySelector('#doc input').required = false
});

//AGREGAR IMG TOGGLE
$('#si_img').click(function() {
    $('.imgs').slideDown(300);
    if (document.querySelector('#img input') != null) document.querySelector('#img input').required = true
});
$('#no_img').click(function() {
    $('.imgs').slideUp(300);
    if (document.querySelector('#img input') != null) document.querySelector('#img input').required = false
});

if (($('#xml .file-name').html() != undefined && $('#xml .file-name').html() != '') || ($('#pdf .file-name').html() != undefined && $('#pdf .file-name').html() != '')) {
    $('#no_doc').prop('checked', false);
    $('#si_doc').prop('checked', true);
    $('.docs').show();
    xml_filename = $('#xml .file-name').text()
    pdf_filename = $('#pdf .file-name').text()
    if ($('#no_doc').click(function() {
        $('.docs').hide();
        $('#xml .file-name').text('')
        $('#pdf .file-name').text('')
    }));
    if ($('#si_doc').click(function() {
        $('.docs').show();
        $('#xml .file-name').text(xml_filename)
        $('#pdf .file-name').text(pdf_filename)
        document.querySelector('#xml input').required = false
        document.querySelector('#pdf input').required = false
    }));
}

if ($('#doc .file-name').html() != undefined && $('#doc .file-name').html() != '') {
    $('#no_doc').prop('checked', false);
    $('#si_doc').prop('checked', true);
    $('.docs').show();
    doc_filename = $('#doc .file-name').text()
    if ($('#no_doc').click(function() {
        $('.docs').hide();
        $('#doc .file-name').text('')
    }));
    if ($('#si_doc').click(function() {
        $('.docs').show();
        $('#doc .file-name').text(doc_filename)
        document.querySelector('#doc input').required = false
    }));
}

if ($('#img .file-name').html() != undefined && $('#img .file-name').html() != '') {
    $('#no_img').prop('checked', false);
    $('#si_img').prop('checked', true);
    $('.imgs').show();
    img_filename = $('#img .file-name').text()
    if ($('#no_img').click(function() {
        $('.imgs').hide();
        $('#img .file-name').text('')
    }));
    if ($('#si_img').click(function() {
        $('.imgs').show();
        $('#img .file-name').text(img_filename)
        document.querySelector('#img input').required = false
    }));
}

//DETALLES TARJETAS FP
$('a.tarjeta-lg.fp').click(function() {
    var id = $(this).attr('id');
    const datos = document.getElementById(id);
    $('#num_factura').html(datos.dataset.num_factura);
    $('#fecha_factura').html(datos.dataset.fecha_factura);
    $('#nom').html(datos.dataset.nom);
    $('#num_pedimento').html(datos.dataset.num_pedimento);
    $('#rfc').html(datos.dataset.rfc);
    $('#fecha_venc').html(datos.dataset.fecha_venc);
    if (datos.dataset.xml != 'None') $('#xml').attr('href', '/verDoc/fp?id='+datos.dataset.xml);
    if (datos.dataset.pdf != 'None') $('#pdf').attr('href', '/verDoc/fp?id='+datos.dataset.pdf);
    $('#editar').attr('href', '/editFP?id='+id)
    $('#borrar').attr('href', '/deleteFP?id='+id)
    
    if (datos.dataset.rfc.length == 0) $('#tr_rfc').hide();
    else $('#tr_rfc').show();
    if (datos.dataset.fecha_venc.length == 0) $('#tr_fecha_venc').hide();
    else $('#tr_fecha_venc').show();
    if (datos.dataset.xml == 'None') $('#tr_xml').hide();
    else $('#tr_xml').show();
    if (datos.dataset.pdf == 'None') $('#tr_pdf').hide();
    else $('#tr_pdf').show();
    $('.modal').addClass('is-active');
});

//DETALLES TARJETAS FC
$('a.tarjeta-lg.fc').click(function() {
    var id = $(this).attr('id');
    const datos = document.getElementById(id);
    $('#num_factura').html(datos.dataset.num_factura);
    $('#fecha_factura').html(datos.dataset.fecha_factura);
    $('#nom').html(datos.dataset.nom);
    $('#num_pedimento').html(datos.dataset.num_pedimento);
    $('#rfc').html(datos.dataset.rfc);
    if (datos.dataset.xml != 'None') $('#xml').attr('href', '/verDoc/fc?id='+datos.dataset.xml);
    if (datos.dataset.pdf != 'None') $('#pdf').attr('href', '/verDoc/fc?id='+datos.dataset.pdf);
    $('#editar').attr('href', '/editFC?id='+id)
    $('#borrar').attr('href', '/deleteFC?id='+id)
    
    if (datos.dataset.rfc.length == 0) $('#tr_rfc').hide();
    else $('#tr_rfc').show();
    if (datos.dataset.xml == 'None') $('#tr_xml').hide();
    else $('#tr_xml').show();
    if (datos.dataset.pdf == 'None') $('#tr_pdf').hide();
    else $('#tr_pdf').show();
    $('.modal').addClass('is-active');
});

//DETALLES TARJETAS CATALOGO
$('a.tarjeta-lg.c').click(function() {
    var id = $(this).attr('id');
    const datos = document.getElementById(id);
    if (datos.dataset.tipo == 'cliente') {
        $('#h_num_registro').html("Número de cliente");
        $('#h_nom').html("Nombre completo de cliente");
    }
    if (datos.dataset.tipo == 'proveedor') {
        $('#h_num_registro').html("Número de proveedor");
        $('#h_nom').html("Nombre de proveedor");
    }
    $('#num_registro').html(datos.dataset.num_registro);
    $('#nom').html(datos.dataset.nom);
    $('#dir').html(datos.dataset.dir);
    $('#tel').html(datos.dataset.tel);
    $('#rfc').html(datos.dataset.rfc);
    $('#correo').html(datos.dataset.correo);
    $('#editar').attr('href', '/editC?id='+id)
    $('#borrar').attr('href', '/deleteC?id='+id)
    
    if (datos.dataset.rfc.length == 0) $('#tr_rfc').hide();
    else $('#tr_rfc').show();
    $('.modal').addClass('is-active');
});

//DETALLES TARJETAS PEDIMENTOS
$('a.tarjeta-lg.p').click(function() {
    var id = $(this).attr('id');
    const datos = document.getElementById(id);
    $('#num_pedimento').html(datos.dataset.num_pedimento);
    $('#fecha_pedimento').html(datos.dataset.fecha_pedimento);
    $('#fecha_venc').html(datos.dataset.fecha_venc);
    $('#material').html(datos.dataset.material);
    $('#aduana').html(datos.dataset.aduana);
    $('#exportador').html(datos.dataset.exportador);
    if (datos.dataset.doc != 'None') $('#doc').attr('href', '/verDoc/p?id='+datos.dataset.doc);
    $('#editar').attr('href', '/editPed?id='+id)
    $('#borrar').attr('href', '/deletePed?id='+id)

    if (datos.dataset.doc == 'None') $('#tr_doc').hide();
    else $('#tr_doc').show();
    $('.modal').addClass('is-active');
});

//DETALLES TARJETAS PL
$('a.tarjeta-lg.pl').click(function() {
    var id = $(this).attr('id');
    const datos = document.getElementById(id);
    $('#num_ref').html(datos.dataset.num_ref);
    $('#nom').html(datos.dataset.nom);
    $('#rfc').html(datos.dataset.rfc);
    $('#fecha_recibido').html(datos.dataset.fecha_recibido);
    $('#fecha_enviado').html(datos.dataset.fecha_enviado);
    if (datos.dataset.doc != 'None') $('#doc').attr('href', '/verDoc/pl?id='+datos.dataset.doc);
    if (datos.dataset.img != 'None') $('#img').attr('href', '/verDoc/pl?id='+datos.dataset.img);
    $('#editar').attr('href', '/editPL?id='+id)
    $('#borrar').attr('href', '/deletePL?id='+id)
    if (datos.dataset.rfc.length == 0) $('#tr_rfc').hide();
    else $('#tr_rfc').show();
    if (datos.dataset.doc == 'None') $('#tr_doc').hide();
    else $('#tr_doc').show();
    if (datos.dataset.img == 'None') $('#tr_img').hide();
    else $('#tr_img').show();
    $('.modal').addClass('is-active');
});

//DETALLES TARJETAS ARCHIVOS
$('a.tarjeta-lg.a').click(function() {
    var id = $(this).attr('id');
    const datos = document.getElementById(id);
    $('#num_ref').html(datos.dataset.num_ref);
    $('#nom').html(datos.dataset.nom);
    $('#fecha').html(datos.dataset.fecha);
    $('#tipo').html(datos.dataset.tipo);
    $('#size').html(datos.dataset.size);
    $('#desc').html(datos.dataset.desc);
    $('#doc').attr('href', '/verDoc/a?id='+datos.dataset.doc);
    $('#editar').attr('href', '/editArchivo?id='+id)
    $('#borrar').attr('href', '/deleteArchivo?id='+id)
    if (datos.dataset.desc.length == 0) $('#tr_desc').hide();
    else $('#tr_desc').show();
    $('.modal').addClass('is-active');
});

//DETALLES TARJETAS USUARIOS
$('a.tarjeta-lg.u').click(function() {
    var id = $(this).attr('id');
    const datos = document.getElementById(id);
    $('#asignacion').html(datos.dataset.asignacion);
    $('#nom').html(datos.dataset.nom);
    $('#password').html(datos.dataset.password);

    check = '<span class="icon is-small has-text-success"><i class="fas fa-check"></i></span>'
    cross = '<span class="icon is-small has-text-danger"><i class="fas fa-times"></i></span>'

    obj = JSON.parse(datos.dataset.roles.replaceAll("'", '"'))
    if (obj.fp.match('c')) $('#fp_c').html(check); else $('#fp_c').html(cross);
    if (obj.fp.match('r')) $('#fp_r').html(check); else $('#fp_r').html(cross);
    if (obj.fp.match('u')) $('#fp_u').html(check); else $('#fp_u').html(cross);
    if (obj.fp.match('d')) $('#fp_d').html(check); else $('#fp_d').html(cross);

    if (obj.fc.match('c')) $('#fc_c').html(check); else $('#fc_c').html(cross);
    if (obj.fc.match('r')) $('#fc_r').html(check); else $('#fc_r').html(cross);
    if (obj.fc.match('u')) $('#fc_u').html(check); else $('#fc_u').html(cross);
    if (obj.fc.match('d')) $('#fc_d').html(check); else $('#fc_d').html(cross);

    if (obj.pedimentos.match('c')) $('#p_c').html(check); else $('#p_c').html(cross);
    if (obj.pedimentos.match('r')) $('#p_r').html(check); else $('#p_r').html(cross);
    if (obj.pedimentos.match('u')) $('#p_u').html(check); else $('#p_u').html(cross);
    if (obj.pedimentos.match('d')) $('#p_d').html(check); else $('#p_d').html(cross);

    if (obj.pl.match('c')) $('#pl_c').html(check); else $('#pl_c').html(cross);
    if (obj.pl.match('r')) $('#pl_r').html(check); else $('#pl_r').html(cross);
    if (obj.pl.match('u')) $('#pl_u').html(check); else $('#pl_u').html(cross);
    if (obj.pl.match('d')) $('#pl_d').html(check); else $('#pl_d').html(cross);

    if (obj.catalogo.match('c')) $('#c_c').html(check); else $('#c_c').html(cross);
    if (obj.catalogo.match('r')) $('#c_r').html(check); else $('#c_r').html(cross);
    if (obj.catalogo.match('u')) $('#c_u').html(check); else $('#c_u').html(cross);
    if (obj.catalogo.match('d')) $('#c_d').html(check); else $('#c_d').html(cross);

    if (obj.archivos.match('c')) $('#a_c').html(check); else $('#a_c').html(cross);
    if (obj.archivos.match('r')) $('#a_r').html(check); else $('#a_r').html(cross);
    if (obj.archivos.match('u')) $('#a_u').html(check); else $('#a_u').html(cross);
    if (obj.archivos.match('d')) $('#a_d').html(check); else $('#a_d').html(cross);

    if (obj.usuarios.match('c')) $('#u_c').html(check); else $('#u_c').html(cross);
    if (obj.usuarios.match('r')) $('#u_r').html(check); else $('#u_r').html(cross);
    if (obj.usuarios.match('u')) $('#u_u').html(check); else $('#u_u').html(cross);
    if (obj.usuarios.match('d')) $('#u_d').html(check); else $('#u_d').html(cross);

    $('#editar').attr('href', '/editUsuario?id='+id)
    $('#borrar').attr('href', '/deleteUsuario?id='+id)
    $('.modal').addClass('is-active');
});

//MANTENER MODAL ABIERTO
var url = document.URL;
var id = url.substring(url.lastIndexOf('?id=') + 4);
const datos = document.getElementById(id);
if (datos) datos.click();

//SELECCION CLIENTE / PROVEEDOR
$('#cop').change( function () {
    var opcion = $(this).val();
    if (opcion == 'cliente') {
        $('#num_registro span').html("Número de cliente");
        $('#nom span').html("Nombre completo de cliente");
    }
    if (opcion == 'proveedor') {
        $('#num_registro span').html("Número de proveedor");
        $('#nom span').html("Nombre de proveedor");
    }
});

$(document).ready(function() {
    $("#cop").trigger('change');
});

//FILTRAR POR CLIENTES / PROVEEDORES
$('#filtro_cop').change( function () {
    var opcion = $(this).val();
    var cont = document.getElementById("cont-tarjetas");
    var tarjeta = cont.getElementsByClassName("tarjeta-lg");
    
    if (opcion == 'clientes') {
        $('#s_num_registro').html("No. de Cliente");
        $('#s_nom').html("Nombre de Cliente");
        for (i = 0; i < tarjeta.length; i++) {
            const datos = tarjeta[i].dataset;
            if (datos.tipo == 'cliente') {
                tarjeta[i].style.display = "";
            } else tarjeta[i].style.display = "none";
        }
    }
    else if (opcion == 'proveedores') {
        $('#s_num_registro').html("No. de Proveedor");
        $('#s_nom').html("Nombre de Proveedor");
        for (i = 0; i < tarjeta.length; i++) {
            const datos = tarjeta[i].dataset;
            if (datos.tipo == 'proveedor') {
                tarjeta[i].style.display = "";
            } else tarjeta[i].style.display = "none";
        }
    }
    else {
        $('#s_num_registro').html("No. de Cliente / Proveedor");
        $('#s_nom').html("Nombre de Cliente / Proveedor");
        for (i = 0; i < tarjeta.length; i++) tarjeta[i].style.display = "";
    }
});

//FILTRAR POR TIPO DOC REPORTE
$('#tipo_doc').change( function () {
    var opcion = $(this).val();

    $('#all').attr("style", "display: none");
    $('input').removeAttr('disabled');

    if (opcion == 'pl'){
        $('#l_fecha').attr("style", "display: none");
        $('#f_fecha_2').attr("style", "display: block");
        $('[name="fecha_2_inicio"]').attr("required", true);
        $('[name="fecha_2_fin"]').attr("required", true);
        $('#l_fecha_r').attr("style", "display: block");
        $('#l_fecha_e').attr("style", "display: block");
        $('#btn_generar').addClass('mt-4');
        $('#btn_generar').removeClass('mt-5');
    } else {
        $('#l_fecha').attr("style", "display: block");
        $('#f_fecha_2').attr("style", "display: none");
        $('[name="fecha_2_inicio"]').removeAttr("required");
        $('[name="fecha_2_fin"]').removeAttr("required");
        $('#l_fecha_r').attr("style", "display: none");
        $('#l_fecha_e').attr("style", "display: none");
        $('#btn_generar').addClass('mt-5');
        $('#btn_generar').removeClass('mt-4');
    }

    if (opcion == 'pedimentos') $('#f_fecha_venc').attr("style", "display: block");
    else $('#f_fecha_venc').attr("style", "display: none");

    if (opcion == 'archivos' || opcion == 'pedimentos') $('#f_p_c').attr("style", "display: none");
    else $('#f_p_c').attr("style", "display: block");

    if (opcion == 'archivos' || opcion == 'pedimentos'){
        $('#p').attr("style", "display: none");
        $('#c').attr("style", "display: none");
    }
    else if (opcion == 'fc'){
        $('#s_p_c').html("Cliente");
        $('#p').attr("style", "display: none");
        $('#c').attr("style", "display: block");
    }
    else {
        $('#s_p_c').html("Proveedor");
        $('#p').attr("style", "display: block");
        $('#c').attr("style", "display: none");
    }
});

//CERRAR MODAL
$('.close').click(function() {
    $('.modal').removeClass('is-active');
    if (url.includes('?id=')) window.location.replace(url.substring(0, url.lastIndexOf('?id=')));
    if (document.getElementsByClassName("password") != null) {
        $('#password').attr("style", '-webkit-text-security: disc !important')
    }
});

$('.modal-card-foot .dropdown .button').click( function () {
    $('.modal-card-foot .dropdown').addClass('is-active');
});

$('.modal-card-foot .dropdown a.button').click( function () {
    $('.modal-card-foot .dropdown').removeClass('is-active');
});

//IFRAME STYLE
var frame = document.querySelector('iframe');
if (frame) frame.onload = function () {
    var body = frame.contentWindow.document.querySelector('body');
    body.style.marginTop = body.style.marginBottom = '0';
    var pre = frame.contentWindow.document.querySelector('pre');
    pre.style.fontSize = '14px';
    pre.style.margin = '0';
};