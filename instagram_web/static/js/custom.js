$(document).ready(function () {
    $.ajaxSetup({
        headers: 
        { 'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content') }
    });

    $(".pendingBtns, .unfollowBtns, .followBtns").on("click", function (e) {
        let id = e.target.id.split("-")[1]
        if ($(`#followBtn-${id}`).html().trim() == "Follow") {
            $.ajax(
                {
                    url: `/following/follow/${id}`,
                    method: "POST",
                    beforeSend: function() {
                        $(e.target)
                        .prop('disabled', true)
                        .text('Loading...')
                        .removeClass("followBtns")
                        .addClass("loadingBtns")
                    }, 
                    success: function (response) {
                        if (response.success) {
                            if (response.status == 'approved') {
                                $(e.target).removeClass("loadingBtns").addClass("unfollowBtns");
                                $(e.target).html("Unfollow").prop('disabled', false);
                            } else {
                                $(e.target).removeClass("loadingBtns").addClass("pendingBtns");
                                $(e.target).html("Pending approval").prop('disabled', false);
                            }
                            $(`#followers_count-${id}`).text(`${response.followers_count}`)
                        }
                    }
                })
        }
        else {
            $.ajax(
                {
                    url: `/following/unfollow/${id}`,
                    method: "POST",
                    beforeSend: function() {
                        if ($(e.target).hasClass("unfollowBtns")){
                            $(e.target).removeClass("unfollowBtns")
                        } else {
                            $(e.target).removeClass("pendingBtns")
                        }
                        $(e.target)
                        .prop('disabled', true)
                        .text('Loading...')
                        .addClass("loadingBtns")
                    }, 
                    success: function (response) {
                        if (response.success) {
                            $(e.target).removeClass("loadingBtns").addClass("followBtns");
                            $(e.target).html("Follow").prop('disabled', false);
                            $(`#followers_count-${id}`).text(`${response.followers_count}`)
                            if (response.is_private) {
                                $(`#picture_container-${id}`).replaceWith(response.private_container)
                            }
                            // userId = $(e.target).closest('.picture_container').attr('data-id')
                            // $(`.picture_container[data-id="${userId}"]`)
                        }
                    }
                }
            )
        }
    })

}) 