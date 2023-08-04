//Tippy ventanas emergentes
document.querySelectorAll('[data-tippy-content]').forEach(x => {
    x.setAttribute('data-tippy-content', i18n.__(x.getAttribute('data-tippy-content')));
    tippy(x, { theme: 'manaflux' });
   });


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('checkAllButton').addEventListener('click', function(e) {
        e.preventDefault();
        checkAll();
    });
    document.getElementById('desmarcar').addEventListener('click', function(e) {
        e.preventDefault();
        uncheckAll();
    });
});

function checkAll() {
    document.querySelectorAll('#atributos input[type=checkbox]').forEach(function(checkElement) {
        checkElement.checked = true;
    });
}

function uncheckAll() {
    document.querySelectorAll('#atributos input[type=checkbox]').forEach(function(checkElement) {
        checkElement.checked = false;
    });
}