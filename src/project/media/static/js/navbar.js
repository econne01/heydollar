var setupModalWindows = function() {
    var triggers = $(".modalInput").overlay({
        // some mask tweaks suitable for modal dialogs
        mask: {
            color: '#ebecff',
            loadSpeed: 200,
            opacity: 0.9
        },
 
        closeOnClick: true
  });
};

setupModalWindows();
