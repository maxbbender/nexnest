function DisplayNotifications(){

    $.each(notifications, function(index, notification) {
    if(notification.message != null){
         var messageContent = notification.message.split("#");
         var newNotification = `<div id="`+ notification.id +`" data-type="`+ notification.notifType +`" data-redirect="`+ notification.redirectURL +`" class="noti">`;
             if(notification.viewed == false){
                 newNotification += `<li class="notification" style="background-color: rgba(86, 134, 197, 0.39);">`;
             }
             else{
                 newNotification += `<li class="notification">`;
             }
                 newNotification += `<div class="media">
                     <div class="media-left vertical-center" style="text-align: center;">
                         <div class="media-object">`;
                             if(notification.notifType == "maintenance"){
                                 newNotification += `<i class="fa fa-wrench fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "tour"){
                                 newNotification += `<i class="fa fa-calendar fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "security_deposit"){
                                 newNotification += `<i class="fa fa-usd fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }    
                             else if(notification.notifType == "group_listing"){
                                 newNotification += `<i class="fa fa-handshake-o fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "house"){
                                 newNotification += `<i class="fa fa-home fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "group_user"){
                                 newNotification += `<i class="fa fa-user fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "group_user_completed"){
                                 newNotification += `<i class="fa fa-user fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "group_listing_favorite"){
                                 newNotification += `<i class="fa fa-star fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "new_tour_time"){
                                 newNotification += `<i class="fa fa-clock-o fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else if(notification.notifType == "rent_reminder"){
                                 newNotification += `<i class="fa fa-usd fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                             else{
                                 newNotification += `<i class="fa fa-bell fa-2x" aria-hidden="true" style="height: 50px; width: 50px; border-radius: 30px;" class="img-circle"></i>`;
                             }
                         newNotification += `</div>
                     </div>
                     <div class="media-body">
                         <strong class="notification-title">`+ messageContent[0] +`</strong>
                         <div class="notification-meta">
                             <div class="row">
                                 <div class="col-xs-8 notification-item-footer">
                                     
                                     <small class="timestamp">`;
                                         if(messageContent.length > 1){
                                             newNotification += messageContent[1] + `-`;
                                         } 
                                         newNotification += moment.utc(notification.date).fromNow() +`</small>
                                 </div>
                             </div>
                         </div>
                     </div>
                 </div>
             </li>
         </div>`;
         $("#notificationArea").append(newNotification);
         }
     });
}