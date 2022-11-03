function toggle_vis(obj) {
    if (obj.src.search('blank') == -1) {
        // Currently visible
        dotpos = obj.src.lastIndexOf('.');
        newsrc = obj.src.slice(0, dotpos) + 'blank' + obj.src.slice(dotpos);
        obj.src = newsrc;
    } else {
        // Currently invisible.
        matres = obj.src.match('(.+)blank(.+)');
        obj.src = matres[1] + matres[2];
    }
}

function show_all_products() {
    var subs = document.getElementsByClassName('sub');
    for (var i = 0; i < subs.length; i++) {
        subs[i].src = "images/" + String(2 * i + 1) + '.png';
    }
}

function toggle_blanks() {
    var butt = document.getElementById('blank-toggler');
    var subs = document.getElementsByClassName('sub');
    const target_display = (butt.innerHTML == 'Hide blanks') ? "none" : "initial";
    for (var i = 0; i < subs.length; i++)
        // The only thing we don't want happening is a visible nonblank turned to a none.
        if (subs[i].src.search('blank') != -1 || subs[i].style.display == 'none')
            subs[i].style.display = target_display;
    butt.innerHTML = (butt.innerHTML == 'Hide blanks') ? 'Show blanks' : 'Hide blanks';
}

function zoom_main(scroll) {
    document.getElementById("main").style.zoom = scroll.value / 100;
}