from django.shortcuts import render
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
from .models import Prediction
import pdfkit
from django.http import HttpResponse
from django.template import loader


def inputData(request):
    context = {'prediction': "0",
               'mileage': "0",
               'enginev': "0.0",
               }
    input_data = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [500,3.0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    if request.method == "POST":
        mileage = request.POST.get("mileage")
        enginev = request.POST.get("enginev")
        brand = request.POST.get("brand")
        body = request.POST.get("body")
        engine = request.POST.get("engine")
        registration = request.POST.get("registration")

        context["mileage"] = mileage
        context["enginev"] = enginev

        input_data[0][0] = int(mileage)
        input_data[0][1] = float(enginev)
        input_data[0][16] = int(registration)

        brand_str = "Audi"
        if brand != "0":
            input_data[0][int(brand)] = 1
            if brand == "2":
                brand_str = "BMW"
            elif brand == "3":
                brand_str = "Mercedes-Benz"
            elif brand == "4":
                brand_str = "Mitsubishi"
            elif brand == "5":
                brand_str = "Renault"
            elif brand == "6":
                brand_str = "Toyota"
            elif brand == "7":
                brand_str = "Volswagen"
        
        body_str = "Crossover"
        if body != "0":
            input_data[0][int(body)] = 1
            if body == "8":
                body_str = "Hatch"
            elif body == "9":
                body_str = "Other"
            elif body == "10":
                body_str = "Sedan"
            elif body == "11":
                body_str = "Vagon"
            elif body == "12":
                body_str = "Van"
        
        engine_str = "Diesel"
        if engine != "0":
            input_data[0][int(engine)] = 1
            if engine == "13":
                engine_str = "Gas"
            elif engine == "14":
                engine_str = "Other"
            elif engine == "15":
                engine_str = "Petrol"

        model = pickle.load(open('cars.sav', 'rb'))

        scaler = StandardScaler()
        scaler.fit(input_data)
        input_scaled = scaler.transform(np.array(input_data))

        pred_price = model.predict(input_scaled)

        actual_pred_price = np.exp(pred_price)

        context['prediction'] = actual_pred_price[0]

        prediction = Prediction(mileage=int(mileage), enginev=float(enginev), brand=brand_str, body=body_str, engine_type=engine_str, registration=int(registration), predicted_price=actual_pred_price[0])
        prediction.save()
        
    return render(request, 'input_data.html', context)


def downloadData(request):
    predictions = Prediction.objects.all()
    context = {'predictions': predictions,}

    template = loader.get_template('download_data.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }
    pdf = pdfkit.from_string(html,False,options)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = "cars.pdf"
    
    return response
