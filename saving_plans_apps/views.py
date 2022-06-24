import json
from dateutil.parser import parse

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from saving_plans_apps.models import User, Plans, Promotions, CustomerGoal


def home(request):
    return HttpResponse("Hello")


@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    name = request.POST.get("name")
    if not name:
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    obj = User.objects.create(name=name)
    obj.save()
    return HttpResponse(json.dumps({"status": True, "message": "User Created Successfully"}),
                        content_type="application/json")


def get_plans(request):
    if request.method != "GET":
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    obj = Plans.objects.all().filter(is_active=True)
    response_dict = []
    for i in obj:
        response_dict.append({"plan_id": i.planId, "plan_name": i.planName,
                              "amount_option": json.loads(i.amountOption), "tenure_option": json.loads(i.tenureOption),
                              "benefit_percentage": i.benefitPercentage, "benefit_types": i.benefitType})
    return HttpResponse(json.dumps({"status": True, "data": response_dict}),
                        content_type="application/json")


def get_promotion(request, plan_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    plan_id = plan_id
    try:
        planObj = Plans.objects.get(planId=plan_id)
    except Plans.DoesNotExist:
        return HttpResponse(json.dumps({"status": False,
                                        "message": "Invalid Request Parameters you have enter the wrong plan id"}),
                            content_type="application/json")
    obj = Promotions.objects.all().filter(planID=planObj)
    response_dict = []
    for i in obj:
        response_dict.append({"plan_id": plan_id, "promotion_Id": i.promotionId,
                              "promotion_type": i.promotionType, "promotion_start_date": str(i.promotionStartDate),
                              "promotion_end_date": str(i.promotionEndDate), "promotion_count": i.promotionCount,
                              "promotion_benefit_percentage": i.promotionBenefitPercentage})
    return HttpResponse(json.dumps({"status": True, "data": response_dict}),
                        content_type="application/json")


def get_customer_goal(request, customer_goal_id):
    if request.method != "GET":
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    customer_goal_id = customer_goal_id
    try:
        customer_obj = CustomerGoal.objects.get(customerId=customer_goal_id)
    except CustomerGoal.DoesNotExist:
        return HttpResponse(json.dumps({"status": False,
                                        "message": "Invalid Request Parameters you have enter the wrong customer goal id"}),
                            content_type="application/json")
    i = customer_obj
    response_dict = [{"plan_id": i.planID.planId, "user_id": i.userID.userID,
                      "promotion_id": i.promotionId, "amount": float(i.amount),
                      "tenure": i.tenure, "start_date": str(i.startDate),
                      "deposit_amount": i.depositAmount, "benefit_percentage": i.benefitPercentage}]
    return HttpResponse(json.dumps({"status": True, "data": response_dict}),
                        content_type="application/json")


@csrf_exempt
def create_plan(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    plan_name = request.POST.get("plan_name")
    amount_options = request.POST.get("amount_options")
    tenure_options = request.POST.get("tenure_options")
    benefit_percentage = request.POST.get("benefit_percentage")
    benefit_type = request.POST.get("benefit_type")

    if not plan_name or not amount_options or not tenure_options or not benefit_percentage or not benefit_type:
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    if not isinstance(json.loads(amount_options), list) and not isinstance(json.loads(tenure_options), list):
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters amount_options and "
                                                                    "tenure_options should be list"}),
                            content_type="application/json")
    obj = Plans.objects.create(
        planName=plan_name,
        amountOption=json.dumps(amount_options),
        tenureOption=json.dumps(tenure_options),
        benefitPercentage=benefit_percentage,
        benefitType=benefit_type
    )
    obj.save()
    return HttpResponse(json.dumps({"status": True, "message": "Plan Created Successfully"}),
                        content_type="application/json")


@csrf_exempt
def create_promotion(request):
    if request.method != "POST":
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    plan_id = request.POST.get("plan_id")
    promotion_type = request.POST.get("promotion_type")
    promotion_start_date = request.POST.get("promotion_start_date")
    promotion_end_date = request.POST.get("promotion_end_date")
    promotion_count = request.POST.get("promotion_count")
    promotion_benefit_percentage = request.POST.get("promotion_benefit_percentage")
    if not plan_id or not promotion_type or not promotion_benefit_percentage:
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    if not (promotion_start_date or promotion_end_date) and not promotion_count:
        return HttpResponse(json.dumps({"status": False,
                                        "message": "Invalid Request Parameters you have to give a start date and end date or the count"}),
                            content_type="application/json")
    try:
        obj2 = Plans.objects.get(planId=plan_id)
    except Plans.DoesNotExist:
        return HttpResponse(json.dumps({"status": False,
                                        "message": "Invalid Request Parameters you have enter the wrong plan id"}),
                            content_type="application/json")
    obj = Promotions.objects.create(
        planID=obj2,
        promotionType=promotion_type,
        promotionStartDate=parse(promotion_start_date) if promotion_start_date else None,
        promotionEndDate=parse(promotion_end_date) if promotion_end_date else None,
        promotionCount=float(promotion_count) if promotion_count else 0,
        promotionBenefitPercentage=promotion_benefit_percentage
    )
    obj.save()
    return HttpResponse(json.dumps({"status": True, "message": "Promotion Created Successfully"}),
                        content_type="application/json")


@csrf_exempt
def create_customer_goal(request, plan_id, user_id):
    if request.method != "POST":
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")
    amount = request.POST.get("amount")
    tenure = request.POST.get("tenure")
    startDate = request.POST.get("start_date")
    deposit_amount = request.POST.get("deposit_amount")
    benefit_percentage = request.POST.get("benefit_percentage")
    promotion_Id = request.POST.get("promotion_id")

    if not amount or not tenure or not startDate or not benefit_percentage or not plan_id or not user_id:
        return HttpResponse(json.dumps({"status": False, "message": "Invalid Request Parameters"}),
                            content_type="application/json")

    try:
        plan_obj = Plans.objects.get(planId=plan_id)
    except Plans.DoesNotExist:
        return HttpResponse(json.dumps({"status": False,
                                        "message": "Invalid Request Parameters you have enter the wrong plan id"}),
                            content_type="application/json")

    try:
        user_obj = User.objects.get(userID=user_id)
    except User.DoesNotExist:
        return HttpResponse(json.dumps({"status": False,
                                        "message": "Invalid Request Parameters you have enter the wrong user id"}),
                            content_type="application/json")
    try:
        promotion_obj = Promotions.objects.get(promotionId=promotion_Id if promotion_Id else 0)
    except Promotions.DoesNotExist:
        if promotion_Id:
            return HttpResponse(json.dumps({"status": False,
                                            "message": "Invalid Request Parameters you have enter the wrong promotion id"}),
                                content_type="application/json")
        promotion_Id = 0
    print(promotion_Id)
    obj = CustomerGoal.objects.create(
        planID=plan_obj,
        userID=user_obj,
        promotionId=promotion_Id,
        benefitPercentage=benefit_percentage,
        amount=float(amount),
        tenure=tenure,
        startDate=parse(startDate),
        depositAmount=float(deposit_amount) if deposit_amount else 0

    )
    obj.save()
    return HttpResponse(json.dumps({"status": True, "message": "Customer Goal Created Successfully"}),
                        content_type="application/json")
