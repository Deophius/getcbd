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

function toggle_intermediates() {
    var subs = document.getElementsByClassName('sub');
    var butt = document.getElementById('all-toggler');
    // Add this stuff after the number.
    const target_prefix = (butt.innerHTML == 'Show all') ? "" : "blank";
    for (var i = 1; i < subs.length - 1; i++) {
        subs[i].src = "images/" + String(2 * i + 1) + target_prefix + '.png';
    }
    butt.innerHTML = (butt.innerHTML == 'Show all') ? 'Hide all' : 'Show all';
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