window.addEventListener("DOMContentLoaded", () => {
    setTimeout(function(){
        var logoutAnchorHrefAttr = "https://keycloak.mendelu.cz/realms/dsw/protocol/openid-connect/logout";
        var logoutAnchorElement = document.querySelector('a[data-cy="menu_logout"]');
        if (logoutAnchorElement) { 
            logoutAnchorElement.setAttribute("href", logoutAnchorHrefAttr);
        }
    }, 3000);
});
