// Import CSS bundle.
require('../sass/main.scss');

require('../img/brand/logo-colorful.v4.svg')
require('../img/brand/logo-green.v2.svg')
require('../img/brand/logo-inverted.svg')
require('../img/brand/logo-rect-green.svg')
require('../img/brand/logo-rect-inverted.svg')
require('../img/brand/logo-rect.svg')
require('../img/brand/logo.svg')
require('../img/brand/ogcapture.png')

// Smooth scrolling
import smoothscroll from 'smoothscroll-polyfill';
smoothscroll.polyfill();

// BulmaJS - initialize JS handlers for the Bulma CSS framework.
// Only the plugins you need
import Navbar from '@vizuaalog/bulmajs/src/plugins/navbar';
import Notification from '@vizuaalog/bulmajs/src/plugins/notification';
import Modal from '@vizuaalog/bulmajs/src/plugins/modal';
// import Tabs from '@vizuaalog/bulmajs/src/plugins/tabs';


// Share modal
document.querySelectorAll('.js-share-modal-trigger').forEach(function(elem) {
    elem.addEventListener('click', function(e) {
        const modal = Modal.create({
            element: document.querySelector('#js-share-modal'),
            style: 'image',
        }).open();
    });
})
