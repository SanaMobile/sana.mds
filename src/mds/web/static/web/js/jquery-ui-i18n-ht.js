/* Kreyol initialisation for the jQuery UI date picker plugin. */
/* Written by 
 */
jQuery(function($){
    $.datepicker.regional['ht'] = {
        closeText: "Sòti",
        prevText: "Anvan",
        nextText: "Pwochen",
        currentText: "Jodi a",
        monthNames: [ 'Janvye', 'Fevriye', 'Mas', 'Avril', 'Me', 'Jwen', 
        'Jiye', 'Out', 'Septanm', 'Oktob', 'Novanm', 'Desanm'],
        monthNamesShort: [ 'Janv', 'Fevr', 'Mas ', 'Avr ', 'Mas ', 'Jwen', 
        'Jiye', 'Out ', 'Sept', 'Okt ', 'Nov ', 'Des '],
        dayNames: [ "dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi" ],
        dayNamesShort: [ "dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam." ],
        dayNamesMin: [ "D","L","M","M","J","V","S" ],
        weekHeader: "Sem.",
        dateFormat: "dd-MM-yy",
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: "" 
    };
    $.datepicker.setDefaults( $.datepicker.regional['ht']);
});
