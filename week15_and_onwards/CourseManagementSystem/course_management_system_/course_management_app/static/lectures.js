/**
 * Created by netherblood on 07.02.17.
 */
"use strict";

var htmltext = "";
var showRegForm;
$(function () {
	//PRODUCTPAGE
	var disp;

  $('.tab-item a').click(function(e){
    e.preventDefault();
     disp = $(this).attr('href');
     $('.tab-item a h4').removeClass("selected");
     $(this).children().addClass('selected');

     switch (disp) {

       case "#course-detail":
       $("#course-reviews").addClass("fadeOut");
       $("#course-detail").removeClass("fadeOut");
       setTimeout( function(){
           $("#course-reviews").css("display","none");
           $("#course-detail").css("display","block");
           $("#course-detail").addClass("fadeIn");
       }, 700);

       break;

       case "#course-reviews":
       $("#course-detail").addClass("fadeOut");
       $("#course-reviews").removeClass("fadeOut");
       setTimeout( function(){
           $("#course-detail").css("display","none");
           $("#course-reviews").css("display","block");
           $("#course-reviews").addClass("fadeIn");
       }, 700);

       break;
     }

  });
	$(".lesson-info").click(function () {
		var header = $(this);

        //getting the next element
		var content = $(header).next();
        return $(content).is(":visible") ? ($(header).children().first().children()[1].src = "http://www.shawacademy.com/user/sites/shawacademy.com/themes/mytheme/images/collapse.png", $(header).children().first().css("background-color","#f6f6f6")) : ($(header).children().first().children()[1].src = "http://www.shawacademy.com/user/sites/shawacademy.com/themes/mytheme/images/expand.png", $(header).children().first().css("background-color","#ffffff"));
        //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
		$(content).slideToggle(500, function () {
			//execute this after slideToggle is done
			//change text of header based on visibility of content div
			return $(content).is(":visible") ? ($(header).children().first().children()[1].src = "http://www.shawacademy.com/user/sites/shawacademy.com/themes/mytheme/images/collapse.png", $(header).children().first().css("background-color","#f6f6f6")) : ($(header).children().first().children()[1].src = "http://www.shawacademy.com/user/sites/shawacademy.com/themes/mytheme/images/expand.png", $(header).children().first().css("background-color","#ffffff"));
		});
    });
	function showRegistrationForm() {
		$("#regFlowError").css('display','none');
		$("#regFlowStep1").css('display','block');
		$("#regFlowStep2").css('display','none');
	}

	if($('.selectIndicator').length) {

    } else {

    }

    $(window).resize(function() {
    	if($('.selectIndicator').length) {

	    } else {

	    }
    });
	//PRODUCTPAGE
	$(".testimonialsSec").tabs({
		show: { effect: "fade", duration: 300 }
	});
	//PRODUCTPAGE
	$(".courseSchedule").tabs({
		show: { effect: "fade", duration: 300 }
	});
	//PRODUCTPAGE
	$(".extras").tabs({
		show: { effect: "fade", duration: 300 }
	});
	//PRODUCTPAGE
	$(".testimonialsSec ul>li").click(function () {
		$(this).addClass('active');
		$(this).siblings().removeClass('active');
	});
	//PRODUCTPAGE
	$("#diplomaCourses ul>li").click(function () {
		$(this).addClass('active');
		$(this).siblings().removeClass('active');
	});
	//PRODUCTPAGE
	$('.extra ul>li').click(function () {
		$(this).addClass('active');
		$(this).siblings().removeClass('active');
	});
	//PRODUCTPAGE
	$('.courseScheduleListItems li').click(function () {
		$(this).find('a').addClass('active');
		$(this).siblings().find('a').removeClass('active');
	});
	//PRODUCTPAGE
	$("#mobileTab").click(function(){
		$(".courseScheduleListItems").toggle();
		$("#mobileTab img").toggleClass('active');
	});
	//PRODUCTPAGE
	$(".mobileTabListItem").click(function(){
		$("#mobileTab span").text($(this).text());
		if( window.innerWidth <=482) {
			$(".courseScheduleListItems").toggle();
			$("#mobileTab img").toggleClass('active');
		}
	});
	//PRODUCTPAGE
	$("#extraTab").click(function(){
		$(".extraListItems").toggle();
		$("#extraTab img").toggleClass('active');
	});
	//PRODUCTPAGE
	$(".extraItems").click(function(){
		$("#extraTab span").text($(this).text());
		if( window.innerWidth <=482) {
			$(".extraListItems").toggle();
			$("#extraTab img").toggleClass('active');
		}
	});
	//PRODUCTPAGE
	$('.courseDetail section a.readMoreCourseDetails').click(function() {
		var count = 0;
		//ellipsisText = "";
		var ellipsisText = "";
		if($('.courseDetialPara').height() == 110) {
			$('.courseDetialPara').css('height', 'auto');
			var textHeight = $('.courseDetialPara').height();
			$('.courseDetialPara').css('height', '110px');
			$('.courseDetialPara').animate({'height': textHeight}, 600);
			$('.courseDetialPara').css('margin-bottom', '0');
			$('.courseDetail section .readMoreCourseDetails').text("Read Less");
			$('.courseDetialPara').addClass("readLess");
			htmltext = $('.courseDetialPara').html();
			$('.courseDetialPara p').each (function (ind) {
				var text = $(this).text();
				ellipsisText = text;
				var substring = "...";
				if(text.indexOf(substring) !== -1) {
					count = ind;
					$(this).text(text.replace("...", ""));
				}
			});

			$('.courseDetialPara p').each (function (ind) {
				if(count == ind) {
					$(this).css('display','inline')
				}
				if(count == (ind -1)) {
					$(this).css('display','inline')
				}
			});
		} else {
			$('.courseDetialPara').css('height', '110');
			$('.courseDetialPara').css('margin-bottom', '9px');
			$('.courseDetail section .readMoreCourseDetails').text("Read More");
			goToByScroll("courseDetailSec");
			$(".courseDetialPara").html(htmltext);
		}
		return false;
	});

	if($('#courseDetailSec').find('a.readMoreCourseDetails').length == 0) {
		$('.courseDetialPara p').each (function () {
				var text = $(this).text();
				var substring = "...";
				if(text.indexOf(substring) !== -1) {
					$(this).text(text.replace("...", ""));
				}
		});
	}
	//PRODUCTPAGE
	$(".write-a-review-icon").click(function(){
		goToByScroll("averageRatingsSection");
	});
	//PRODUCTPAGE
	$('.productTop > a').click(function() {
		showDiplomaCourses();
		return false;
	});
	//PRODUCTPAGE

	$('#freeTrial').click(function () {
		$('#coursePageFreeTrial').submit();
	});

	$('#regFlowPopupTrigger').magnificPopup({
		type: 'inline',
		removalDelay: 500,
		callbacks: {
			beforeOpen: function() {
				this.st.mainClass = this.st.el.attr('data-effect');
			},
			open: function(){
			}
		},
		midClick: true
	});
	$('.chooseLevel a.chooseLevelOption').click(function() {
		clearTimeout(showRegForm);
		if(schedules){
			$('#regFlowPopupTrigger').click();
			showRegistrationForm();
		} else {
		    var magnificPopup = $.magnificPopup.instance;
			magnificPopup.close();
			$('#trialform').submit();
		}
	});
	//PRODUCT_PAGE
	$('.free-trial-start-btn').magnificPopup({
		type: 'inline',
		removalDelay: 500,
		callbacks: {
			beforeOpen: function() {
				this.st.mainClass = this.st.el.attr('data-effect');
			},
			open: function(){
			}
		},
		midClick: true
	});
	//PRODUCT
	$(".more-date").click(function(event){
		var statusCurrent=$(this).children(".more-dropdown").hasClass("show-more-dropdown");
		$.each($('.more-dropdown'), function (i, ele) {
				$(ele).removeClass('show-more-dropdown');
				$(ele).parent().find(".arrow").removeClass("animateArrow");
		});
		if(statusCurrent){
			$(this).children(".more-dropdown").removeClass('show-more-dropdown');
			$(this).children(".arrow").removeClass("animateArrow");
		}else {
			$(this).children(".more-dropdown").addClass('show-more-dropdown');
			$(this).children(".arrow").addClass("animateArrow");
		}
		event.preventDefault();
	});
	//PRODUCT_PAGE
	if(freeOrPaid=='free'){
		showRegForm = setTimeout(function() {
		   $.magnificPopup.open({
		    items: {
		        src: '#regFlowPopup'
		    },
		    type: 'inline'
		      });
		 }, 90000);
	}
	var selectedSortScheme = 'popular';
    var page = 1;
    var isEmpty = false;
    function getPriceAttribute(pricingData,countryCode, attribute){
    	return pricingData[countryCode.toLowerCase()] ? pricingData[countryCode.toLowerCase()][attribute] : pricingData["default"][attribute];
    }
    function handleSinglePaymentLink(countryCode){
	    var cur_symbol = getPriceAttribute(pricingDetails.header,countryCode,'cur_symbol');
    	var cur_code = getPriceAttribute(pricingDetails.header,countryCode,'currency_code');
    	var price = getPriceAttribute(pricingDetails.header,countryCode,'price');
    	var offerPrice = getPriceAttribute(pricingDetails.header,countryCode,'offer-price');
    	var priceLink = priceLinks[cur_code];
    	var currentLocationBase64=btoa(window.location.href);
    	if(price && priceLink){
            if(freeOrPaid =='paid') {
            	$(".chooseLevel .price-value").html(cur_symbol+ " "+price);
            	if(offerPrice){
            		$(".chooseLevel .offer-price-value").html(cur_symbol+ " "+offerPrice);
            	}
            	var paramSeparator="?";
            	if(priceLink.indexOf("?")>0){
            		paramSeparator="&";
            	}
            	// console.log(paramSeparator, priceLink);
            	$(".chooseLevel a").attr("href", priceLink+ paramSeparator+"event=link-clicked&event_type=payment-link&course="+courseId+"&uid=undefined&currency_link="+currentLocationBase64);
            	$(".chooseLevel a.choosePayment").attr("data-price",price);
            	$(".chooseLevel a.choosePayment").attr("data-gaaction",gaActionPayment+"-"+cur_code);
            }
    	} else {
    		$(".chooseLevel a").attr("href", $(".chooseLevel a").attr("href")+currentLocationBase64);
    	}
	}
	function displayShawPayment(pricingDataObject,priceLinksObject,className){
		var cur_symbol = getPriceAttribute(pricingDataObject,countryCode,'cur_symbol');
    	var cur_code = getPriceAttribute(pricingDataObject,countryCode,'currency_code');
    	var price = getPriceAttribute(pricingDataObject,countryCode,'price');
    	var priceLink = priceLinksObject[cur_code];
    	var currentLocationBase64=btoa(window.location.href);
    	if(price && priceLink){
	    	$(".scrollHeader."+className+" .mini-offer-price sup").text(cur_symbol);
    		$(".scrollHeader."+className+" .mini-offer-price h5").text(price);
		    var paramSeparator="?";
        	if(priceLink.indexOf("?")>0){
        		paramSeparator="&";
        	}
    		$(".scrollHeader."+className+" .mini-upgrade-cta a").attr("href", priceLink+ paramSeparator+"event=link-clicked&event_type=payment-link&course="+courseId+"&uid=undefined&currency_link="+currentLocationBase64);
    		$(".scrollHeader."+className+" .mini-upgrade-cta a").attr("data-gaaction",gaActionPayment+"-"+cur_code);
    	}
	}
    function handleShawPaymentLinks(countryCode, key,months){
		var pricingDataObject=pricingDetails.header[key];
        var priceLinksObject=priceLinks[key];
        var className=key;
        displayShawPayment(pricingDataObject,priceLinksObject,className,countryCode,months);
    }
	function handleSalesPaymentLinks(countryCode){
		handleShawPaymentLinks(countryCode,"pricesOneMonth",1);
    	handleShawPaymentLinks(countryCode,"pricesThreeMonth",3);
    	handleShawPaymentLinks(countryCode,"pricesSixMonth",6);
    	handleShawPaymentLinks(countryCode,"pricesTwelveMonth",12);
	}
	function padToTwo(number) {
  		return ("00"+number).slice(-2);
	}
    function displayAftPayment(pricingDataObject,priceLinksObject,className,countryCode, months){
        var cur_symbol = getPriceAttribute(pricingDataObject,countryCode,'cur_symbol');
        var cur_code = getPriceAttribute(pricingDataObject,countryCode,'currency_code');
        var price = getPriceAttribute(pricingDataObject,countryCode,'price');
        var priceLink = priceLinksObject[cur_code];
        var currentLocationBase64=btoa(window.location.href);
        if(price && priceLink){
            $(".scrollHeader."+className+" .mini-offer-price sup").text(cur_symbol);
            $(".header."+className+" .offer-price sup").text(cur_symbol);

            $(".scrollHeader."+className+" .mini-offer-price h5").text(Math.floor(price/months));
            var firstPart=Math.floor(price/months);
            var remaining=Number(price-firstPart).toFixed(2);

            $(".header."+className+" .offer-price h2").text(firstPart);
            $(".header."+className+" .offer-price p").html("."+padToTwo(remaining)+"<br/>/Month");
            var paramSeparator="?";
            if(priceLink.indexOf("?")>0){
                paramSeparator="&";
            }
            $(".scrollHeader."+className+" .mini-upgrade-cta a").attr("href", priceLink+ paramSeparator+"event=link-clicked&event_type=payment-link&course="+courseId+"&uid=undefined&currency_link="+currentLocationBase64);
            $(".scrollHeader."+className+" .mini-upgrade-cta a").attr("data-gaaction",gaActionPayment+"-"+cur_code);
            $(".header."+className+" .upgrade-cta a").attr("href", priceLink+ paramSeparator+"event=link-clicked&event_type=payment-link&course="+courseId+"&uid=undefined&currency_link="+currentLocationBase64);
            $(".header."+className+" .upgrade-cta a").attr("data-gaaction",gaActionPayment+"-"+cur_code);
        }
    }
    function handleAftPaymentLinks(countryCode, key,months){
		var pricingDataObject=pricingDetails.header[key];
        var priceLinksObject=priceLinks[key];
        var className=key;
        displayAftPayment(pricingDataObject,priceLinksObject,className,countryCode,months);
    }
    function handleAftSalesPaymentLinks(countryCode){
    	handleAftPaymentLinks(countryCode,"pricesOnePart",1);
    	handleAftPaymentLinks(countryCode,"pricesTwoPart",2);
    	handleAftPaymentLinks(countryCode,"pricesFourPart",4);
    }
    detectCountry(function(countryCode){
    	if(pricingDetails){
	        if(priceLinks){
	        	if(type=="sales-campaign-multiple-payment"){
	        		handleSalesPaymentLinks(countryCode)
	        	} else if(type=="aft-sales-campaign-multiple-payment"){
	        		handleAftSalesPaymentLinks(countryCode)
	        	} else {
	        		handleSinglePaymentLink(countryCode);
	        	}
	        }
    	}

        var shawTimeZone=getShawTimezone(countryCode);
        var scheduleDisplay;
        var scheduleDisplayDefault;
        if(schedules){
    		schedules.forEach(function(schedule) {
    			if(schedule.courseTimeZone===shawTimeZone){
    				scheduleDisplay=schedule;
    			}
    			if(schedule.courseTimeZone==='GMT') {
    				scheduleDisplayDefault=schedule;
    			}
    		});
		}
		if(!scheduleDisplay){
			scheduleDisplay=scheduleDisplayDefault;
		}
		var index=0;
        //figure which schedule to show
        if(scheduleDisplay && scheduleDisplay.lessonDates){
	       	$(".on-demand-course-true").each(function(index,elem){
	       		var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' ,'hour':'numeric', 'minute': 'numeric'};
	       		var timeOnly =new Date(scheduleDisplay.lessonDates[index]+ " "+scheduleDisplay.courseStartTime + " GMT");
	       		var locale=navigator.language;
	       		var dateString=timeOnly.toLocaleDateString(locale, options);
	       		if(dateString!='Invalid Date'){
	       			var htmlString=dateString;
	       			$(elem).html(htmlString);
	       		}
				index++;
	        });
       	}
    });
    function renderTemplate(templateVar) {
        _.templateSettings.variable = "review_res";
        var reviewsTemplate = _.template(
            $('#productInlineTestimonialTemplate').html()
        );
        var selectorId;
        if(selectedSortScheme === 'new'){
            selectorId = '#newTestimonials';
        }
        else{
            selectorId = '#topTestimonials';
        }

        $(selectorId).html(
            reviewsTemplate(templateVar)
        );
    }
    $('.nextPage').click(function () {
        if(!isEmpty){
            var filterParam = {facets: '*', filters: 'courseIds: '+ courseId, page: page, hitsPerPage: 5};
            doAlgoliaSearchOnIndex('reviews_'+selectedSortScheme, filterParam, function(err, content){
                page += 1;
                if(content.hits.length){
                    var options = { day: 'numeric', month: 'short', year: 'numeric'};
                    var locale = language === 'en' ? language + '-IN' : language+'-'+language.toUpperCase();
                    $.each(content.hits, function (i, reviews) {
                        var createdDate = new Date(reviews.created);
                        reviews.created = language === 'en' ? createdDate.toLocaleDateString(locale, options).split(' ').join('-') : createdDate.toLocaleDateString(locale, options);
                    });
                    renderTemplate(content.hits);
                }
                else{
                    isEmpty = true;
                    $('.nextPage').hide();
                }
            });
        }
    });
});
var contactNumber=$("#regForm1 #phone");
createTelephoneInput(contactNumber);
function regFlowStep1FormValidate(contactNumber){
    var isFormValid = true;
    if($('#regForm1 input[name=name]').val() === '' ){
        markMandatory($('#regForm1 #name'));
        //$('#name').css('border-bottom', '2px solid #e45555');
        isFormValid = false;
    }
    else{
        $('#regForm1 #name').css('border-bottom', '1px solid #bbb');
    }
    if(!validateEmail($('#regForm1 input[name=email]').val())){
        markMandatory($('#regForm1 #email'));
        isFormValid = false;
    }
    else{
        $('#regForm1 #email').css('border-bottom', '1px solid #bbb');
    }
    if(contactNumber.val() === '' ||  !contactNumber.intlTelInput("isValidNumber")){
        markMandatory($('#phone'));
        isFormValid = false;
    }
    else {
        $('#regForm1 #phone').css('border-bottom', '1px solid #bbb');
    }


    return isFormValid;
}
function regFlowStep2FormValidate(){
    var isFormValid = true;
    $("#regForm2 select").each(function() {
		var id = '';
		id ="#"+this.id;
		if(this.value === '') {
			markMandatory($('#regForm2 '+id));
	        isFormValid = false;
		}
		else{
	        $('#regForm2 '+id).css('border-bottom', '1px solid #bbb');
	    }
	});
	if($('#regForm2 input[name=password]').val() === '' ){
        markMandatory($('#regForm2 #password'));
        isFormValid = false;
    }
    else{
        $('#regForm2 #password').css('border-bottom', '1px solid #bbb');
    }
    return isFormValid;
}
function updateDataLayerForRegistrationSuccess(choosenCampaignId, userEvent){
	var courseStartDate='';
	var courseStartDateTz='';
	if(foundationSchedules){
		foundationSchedules.forEach(function(schedule) {
			if(schedule.campaignId===choosenCampaignId){
				courseStartDate=new Date(schedule.courseStartDate);
				courseStartDateTz=schedule.courseStartDate+'-'+schedule.courseTimeZone;
			}
		});
	}
	var registrationDate=new Date();
	var oneDay = 24*60*60*1000;
	var diffDays = Math.round(Math.abs((registrationDate.getTime() - courseStartDate.getTime())/(oneDay)));
    var google_tag_params = {
	    'edu_pid': courseId,
	    'edu_language': language,
	    'edu_plocid': gravityConfig.locationData.city,
	    'edu_pagetype': pageType,
	    'edu_courseStartDate': courseStartDateTz,
	    'edu_registration_step': userEvent,
		'edu_registration_date': registrationDate.toUTCString(),
		'edu_time_to_course': diffDays,
	    'eventCreatedDate': new Date().toUTCString()
    };
    dataLayer.push({'event':'d_rmkt','google_tag_params': google_tag_params});
}
$("#regForm2 button").click(function(e){
	var gravityData=JSON.parse(gravityCookieData)
	var leadId=gravityData.leadId;
	var regisrationId="";
	if(gravityData.registrations && gravityData.registrations.length>0 ){
		regisrationId=gravityData.registrations[gravityData.registrations.length-1].id;
	}
	var profileFieldDataArray=[];
	var isFormValid = regFlowStep2FormValidate();
	if(isFormValid){
		$("#regForm2 select").each(function() {
			profileFieldDataArray.push({
				"registration_id": regisrationId,
				"key": this.id,
				"value": this.value
			});
		});
		var formData=JSON.stringify({
			items: profileFieldDataArray
		});
		$.ajax({
	    	"type": 'POST',
	    	"url": 'https://liveapi.academyft.com/v1/leads/'+leadId+"/profile",
	    	"crossDomain": true,
	    	"data": formData,
	    	"contentType": "application/json; charset=utf-8",
	    	"dataType": "json",
	    	success: function(responseData, textStatus, jqXHR) {
	    		//push info into datalayer
	    		updateDataLayerForRegistrationSuccess(campaignId,'onRegistrationStep2Success');
	        	$("#login_email").val(gravityData.email);
	        	$("#login_password").val($('#regForm2 input[name=password]').val());
	        	$("#campaign_id").val(campaignId);
	        	var profileFieldWithPasswordDataArray = {
					"password":$("#regForm2 #password").val(),
					"email":gravityData.email
				};

				var formDataWithPassword=JSON.stringify(profileFieldWithPasswordDataArray);
	        	$.ajax({
			    	"type": 'POST',
			    	"url": 'https://liveapi.academyft.com/v1/users',
			    	"crossDomain": true,
			    	"data": formDataWithPassword,
			    	"contentType": "application/json; charset=utf-8",
			    	"dataType": "json",
			    	success: function(responseData, textStatus, jqXHR) {
			        	$("#shawLoginForm").submit();
			    	},
			    	error: function (responseData, textStatus, errorThrown) {
			        	console.log(responseData, textStatus, errorThrown);
			    	}
				});
	    	},
	    	error: function (responseData, textStatus, errorThrown) {
	        	console.log(responseData, textStatus, errorThrown);
	    	}
		});
	}
});
var gravityCookieData;
var password;
function onRegistrationStep1Success(responseData){
	gravityCookieData=JSON.stringify({
		leadId: responseData.data.id,
		email: responseData.data.email,
		registrations: responseData.data.registrations
	});
	createCookie("gravity", gravityCookieData);
	createCookie("shawacademy_email", responseData.data.email);
	createCookie("shawacademy_leadId", responseData.data.id);
	if (readCookie("gravity_created") === null) {
		createCookie("gravity_created", new Date().getTime());
	}
    $('.regForm h2').text('Finish your Profile');
    $('#regFlowStep1').css({'display': 'none'});
	$('#regFlowStep2').css({'display': 'block'});
	$('.regForm .regFlowStep1').removeClass('active');
	$('.regForm .regFlowStep2').addClass('active');
	updateDataLayerForRegistrationSuccess(campaignId,'onRegistrationStep1Success')
}
var campaignId="";
var defaultCampaignId="";
var isSubmittedForm1 = false;
$("#regFlowStep1 button").click(function(e){
        e.preventDefault();
        var isFormValid = regFlowStep1FormValidate(contactNumber);
        if(isFormValid && !isSubmittedForm1) {
			isSubmittedForm1 = true;
        	detectCountry(function(countryCode, gravityConfig){
        		//figure the timezone + campaign_id
        		var shawTimeZone=getShawTimezone(countryCode);
        		if(foundationSchedules){
	        		foundationSchedules.forEach(function(schedule) {
	        			if(schedule.courseTimeZone===shawTimeZone){
	        				campaignId=schedule.campaignId;
	        			}
	        			if(schedule.courseTimeZone==='GMT') {
	        				defaultCampaignId=schedule.campaignId;
	        			}
	        		});
        		}
        		if(campaignId.length==0) {
        			campaignId=defaultCampaignId;
        		}
        		var actualFormData={};
        		$("#regForm1 input").each(function() {
        			actualFormData[this.id]=this.value;
				});
				var names=actualFormData.name.split(" ");
				var firstName=names[0];
				names[0]="";
				var lastName=names.join(" ").trim();
				if(lastName.length==0){
					lastName=".";
				}
	        	var formData=JSON.stringify({
	        		first_name: firstName,
	        		last_name: lastName,
	        		email: actualFormData.email,
	        		phone: actualFormData.phone,
	        		country: gravityConfig.countryCode,
	        		timezone: gravityConfig.time_zone,
	        		org: "shaw",
	        		campaign_id: campaignId,
					language_id: language
	        	});
	        	password=actualFormData.password;
	        	$.ajax({
			    	"type": 'POST',
			    	"url": 'https://liveapi.academyft.com/v1/freeTrialSignup/',
			    	"crossDomain": true,
			    	"data": formData,
			    	headers: {
				        //"utmzfv": readCookie("__utmz_first_visit"),
				        //"utmz": readCookie("__utmz"),
				        //"utma": readCookie("__utma")
				    },
			    	"contentType": "application/json; charset=utf-8",
			    	"dataType": "json",
			    	success: function(responseData, textStatus, jqXHR) {
			    		onRegistrationStep1Success(responseData);
			    	},
			    	error: function (responseData, textStatus, errorThrown) {
					    $('#regFlowStep1').css({'display': 'none'});
						$('#regFlowStep2').css({'display': 'none'});
						$('#regFlowError').css({'display': 'block'});
						$(".hideForError").hide();

			    	}
				});
	        });
        }
    });

function autoPopulateCourseList() {
	fetchCourseList(function(err, courseList){
			//var defaultOptionElement = $('<option value="" disabled selected>Select a Country</option>');
			//$('#course').append(defaultOptionElement);
			$.each(courseList, function (i, course) {
			courseList.push({id: course.courseId, skill: course.taxonomy.skill, courseDisplayName: course.certificateType + ' in ' + course.courseName});
			var element = $('<option></option>');
			element.val(course.courseId);
			element.text(course.certificateType + ' in ' + course.courseName);
			element.data("skill", course.taxonomy.skill);
			$('#course').append(element);
		});
		$("#course").select2({
			placeholder: "Select a Course",
			dropdownParent: $('#write-review-popup-prod')
		});
	});
}
autoPopulateCourseList();

function rating() {
    var userRating = 0;
    this.setRating = function(rating) {
        userRating = rating;
    }
    this.getRating = function() {
        return userRating;
    }
}
var ratingObj = new rating();

$('.ratingPointButton').click(function (e) {


    var skill = "";
    var courseId = $('#writeReviewForm #course').val();
    var description = "";
    var rating = ratingObj.getRating();
    var userAbout = "";
    var userName = "";


    detectCountry(function(countryCode){
        //TODO: get all the parameters from UI.
        var review=getAlgoliaReviewObject(description, skill, countryCode,userName, userAbout, courseId, rating)
        addObjectToIndex("reviews",review,function(err, content){
            if (err) {
                console.error(err);
                return;
            } else {
                //TODO: do something about it.
            }
        });
    });
});
function fillColorToRatingIcons(rating) {
    $(".writeAReviewImages span" ).each(function(i, ele ) {
        $(ele).removeClass('writeAReviewImagesactive');
    });
    for(var i=0;i< rating; i++) {
        var index = i +1;
        $("#reviewRating"+index).addClass('writeAReviewImagesactive');
        $("#popupReviewRating"+index).addClass('writeAReviewImagesactive');
    }
}
function giveRatingByClickingRatingImage(rating) {
   fillColorToRatingIcons(rating);
   ratingObj.setRating(rating);
   $("#rating").val(rating);
}