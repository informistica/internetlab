# Create your views here.
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Laboratory, Computer
from .forms import LaboratorySelectionForm
import subprocess

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