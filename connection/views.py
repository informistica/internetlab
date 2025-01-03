# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Laboratory, Computer
from .forms import LaboratorySelectionForm
import subprocess
import openpyxl

def laboratory_selection(request):
    if request.method == "POST":
        form = LaboratorySelectionForm(request.POST)
        if form.is_valid():
            lab_id = form.cleaned_data['laboratory'].id
            return redirect('connection:manage_laboratory', lab_id=lab_id)
    else:
        form = LaboratorySelectionForm()

    return render(request, 'laboratory_selection.html', {'form': form})

def manage_laboratory(request, lab_id):
    laboratory = get_object_or_404(Laboratory, id=lab_id)
    computers = laboratory.computers.all()
    # Aggiungi i colori dinamici al contesto
    for computer in computers:
        computer.color = "red" if computer.status == "blocked" else "green"
        computer.button_text = "Sblocca" if computer.status == "blocked" else "Blocca"
    return render(request, 'manage_laboratory.html', {'laboratory': laboratory, 'computers': computers})

def toggle_computer(request, computer_id, action):
    computer = get_object_or_404(Computer, id=computer_id)
    mac = computer.mac_address

    if action == "block":
        computer.status = "blocked"
        #subprocess.run(["/path/to/block_pc.sh", mac])
        print(f"Blocco {computer.name}")
        #return JsonResponse({"status": "blocked", "computer": computer.name})
    elif action == "unblock":
        computer.status = "unblocked"
        #subprocess.run(["/path/to/unblock_pc.sh", mac])
        print(f"Sblocco {computer.name}")
    
    return JsonResponse({"computer": computer.name, "status": computer.status})

def toggle_all_computers(request, laboratory_id, action):
    laboratory = get_object_or_404(Laboratory, id=laboratory_id)
    computers = laboratory.computers.all()

    if action == "block":
        computers.update(status="blocked")
        message = "Tutti i computer sono stati bloccati."
    elif action == "unblock":
        computers.update(status="unblocked")
        message = "Tutti i computer sono stati sbloccati."
    else:
        return JsonResponse({"error": "Azione non valida"}, status=400)

    return JsonResponse({
        "message": message,
        "computers": [{"id": computer.id, "status": computer.status} for computer in computers]
    })

def upload_computers(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                laboratory_name, computer_name, mac_address = row

                # Crea o recupera il laboratorio
                laboratory, created = Laboratory.objects.get_or_create(name=laboratory_name)

                # Crea o aggiorna il computer
                Computer.objects.update_or_create(
                    name=computer_name,
                    laboratory=laboratory,
                    defaults={"mac_address": mac_address},
                )

            messages.success(request, "I dati sono stati caricati con successo.")
        except Exception as e:
            messages.error(request, f"Errore durante il caricamento: {e}")
        
        return redirect("connection:upload_computers")

    return render(request, "upload_computers.html")