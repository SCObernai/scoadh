{% load static %}	

$.getScript("{% static 'adh/cart_mgr.js' %}" )
  .done(function( script, textStatus ) {
    let sco_adh=ScoAdh.prototype.single();
    if (sco_adh.debug) console.log(`ScoAdh - load cart_mgr.js - status : ${textStatus}`);
    let cart_mgr=new ScoAdhCartManager(sco_adh.rootUrl, sco_adh.debug);
    sco_adh.cart_mgr=cart_mgr;
    cart_mgr.initOnDocReady();

    $.getScript( "{% static 'act/act_mgr.js' %}" )
      .done(function( script, textStatus ) {
        let sco_adh=ScoAdh.prototype.single();
        if (sco_adh.debug) console.log(`ScoAdh - load act_mgr.js - status : ${textStatus}`);
        let act_mgr=new ScoAdhActivityManager(sco_adh.rootUrl, sco_adh.debug, cart_mgr);
        sco_adh.act_mgr=act_mgr;
        act_mgr.refillDropDown();

      })
      .fail(function( jqxhr, settings, exception ) {
        console.log(`ScoAdhSystemSettings - load act_mgr.js - ${jqxhr} exception : ${exception}`);
    });



  })
  .fail(function( jqxhr, settings, exception ) {
    console.log(`ScoAdhSystemSettings - load cart_mgr.js - ${jqxhr} exception : ${exception}`);
});


function ScoAdh() {
  return new ScoAdh(false);
}

function ScoAdh(debug) {
    // ----- on fait un singleton pour stocker les params
    if (ScoAdh.prototype._instance) {
      if (debug) 
        console.log(`ScoAdh init - proto inst exists : ${ScoAdhCartManager.prototype._instances}`);
      // -- ici on bypasse le constructeur si le singleton existe déjà
      return ScoAdh.prototype._instance;
    } 
  
    if (debug) 
      console.log(`ScoAdh init - proto inst does NOT exist`);    
    ScoAdh.prototype._instance=this;

    // -- c'est parti pour l'init !

    // Params
    this.debug=false;
    this.rootUrl="{{ rootUrl }}";

}

ScoAdh.prototype.single = function () {
  return new ScoAdh();
}

