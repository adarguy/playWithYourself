// For file browser
$(function() {
// We can attach the `fileselect` event to all file inputs on the page
    $(document).on('change', ':file', function() {
        var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        input.trigger('fileselect', [numFiles, label]);
        document.getElementById("browse").submit();
        setTimeout(function(){
            $("input[name='optradio']").attr("disabled", false);
            $("button[name='buttons']").attr("disabled", false);
        },10000);
        
    });

    // We can watch for our custom `fileselect` event like this
    $(document).ready( function() {
        $(':file').on('fileselect', function(event, numFiles, label) {

            var input = $(this).parents('.input-group').find(':text'),
            log = numFiles > 1 ? numFiles + ' files selected' : label;

            if( input.length ) {
                input.val(log);
            } else {
                if( log ) alert(log);
            }
        });
    });
});

$(document).ready(function() {
    $(".slider").slider();
    $(".slider").on('slide', function(slideEvt) {
        $("#"+this.id+"SliderVal").text(slideEvt.value);
    });

});

function show_hide(id){
    if(document.getElementById(id).style.display == "none"){
        document.getElementById(id).style.display = "";
    }
    else{
        document.getElementById(id).style.display = "none";
    }
}

function inst_show(){

    d = document.getElementById('inst_list');
    //if(d.classList.contains("hidden-xs")){
    d.classList.remove("hidden-xs");
    d.className += " col-xs-12";
    //}
    //else{
    //    d.classList.remove("col-xs-12");
    //    d.className += " hidden-xs";
    //}
}

function clearInput(id){    
    document.getElementById("inst_box"+id).value= "";
    showList(id);
}

function noInput(id){    
    var input = document.getElementById("inst_box"+id);
    if (input.value == ""){  
        input.style.backgroundColor = "#ffcccc"; 
    }else{
        input.style.backgroundColor = "#ffffff";   
    }
}

function instrument_search(id) {
    showList(id);
    var input, filter, ul, li, a, i;
    input = document.getElementById("inst_box"+id);
    filter = input.value.toUpperCase();
    ul = document.getElementById("inst_list"+id);
    li = ul.getElementsByTagName("li"); k=0;
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            if(i%9 != 0){
               li[i].style.display = "";
                if (k!=8){
                    $('#'+li[i].parentNode.getAttribute('id')).collapse('show');
                }
            }           
        } else {
            if (i%9 == 0){
                k=0;
            }
            else{
                li[i].style.display = "none"; k++;
                if (k==8){
                    $('#'+li[i].parentNode.getAttribute('id')).collapse('hide');
                    console.log(li[i].parentNode.getAttribute('id'));
                }
            }
        }
    }
    $(".inst_choice"+id).click(function(){
        document.getElementById("inst_box"+id).value = this.innerHTML;
        document.getElementById("inst"+id).value = this.innerHTML;
        for (i = 0; i < li.length; i++) {
            li[i].style.display = "";
        }
    });
}

$(document).foundation().foundation('joyride', 'start');

var a = audiojs;
a.events.ready(function() {
    var a1 = a.createAll();
});
