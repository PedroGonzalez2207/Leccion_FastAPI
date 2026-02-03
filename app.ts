import { Component, OnInit, signal, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  protected readonly title = signal('Angular');
  private platformId = inject(PLATFORM_ID);

  private readonly API = "http://127.0.0.1:8000/api/matriculas";

  private $ = (id: string) => {
    const element = document.getElementById(id);
    if (!element) throw new Error(`Element with id "${id}" not found`);
    return element as HTMLInputElement;
  };

  private async listar() {
    const res = await fetch(this.API);
    const data = await res.json();
    this.$("listado").textContent = JSON.stringify(data, null, 2);
  }

  private async crear() {
    const placa = this.$("placa").value.trim();
    const propietario = this.$("propietario").value.trim();
    const marca = this.$("marca").value.trim();
    const fabricacion = parseInt(this.$("fabricacion").value.trim());
    const valor_comercial = parseFloat(this.$("valor_comercial").value.trim());

    let impuesto = valor_comercial * 0.025; 
    if (fabricacion < 2010) {
      impuesto = valor_comercial * 0.10;
    }

    const vocales = /^[aeiouAEIOU]/;
    if (vocales.test(marca)) {
      impuesto = Math.max(0, impuesto - 30);
    }

    const codigo_revision = placa.substring(0, 3) + propietario.length + fabricacion.toString().slice(-1);

    const body = {
      placa: placa,
      propietario: propietario,
      marca: marca,
      fabricacion: fabricacion,
      valor_comercial: valor_comercial,
      impuesto: impuesto,
      codigo_revision: codigo_revision,
    };

    const res = await fetch(this.API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json();
    alert("Respuesta: " + JSON.stringify(data));
    await this.listar();
  }

  private async buscar() {
    const placa = this.$("placaBuscar").value.trim();
    const res = await fetch(`${this.API}/${placa}`);
    const data = await res.json();
    this.$("resultadoBuscar").textContent = JSON.stringify(data, null, 2);
  }

  private async actualizar() {
    const placa = this.$("placaUpd").value.trim();

    const body: { [key: string]: string } = {};
    const propietario = this.$("propietarioUpd").value.trim();
    const marca = this.$("marcaUpd").value.trim();
    if (propietario) body["propietario"] = propietario;
    if (marca) body["marca"] = marca;

    const res = await fetch(`${this.API}/${placa}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json();
    alert("Respuesta: " + JSON.stringify(data));
    await this.listar();
  }

  private async eliminar() {
    const placa = this.$("placaDel").value.trim();

    const res = await fetch(`${this.API}/${placa}`, { method: "DELETE" });
    const data = await res.json();
    alert("Respuesta: " + JSON.stringify(data));
    await this.listar();
  }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.$("btnListar").addEventListener("click", () => this.listar());
      this.$("btnCrear").addEventListener("click", () => this.crear());
      this.$("btnBuscar").addEventListener("click", () => this.buscar());
      this.$("btnActualizar").addEventListener("click", () => this.actualizar());
      this.$("btnEliminar").addEventListener("click", () => this.eliminar());

      this.listar().catch(console.error);
    }
  }
}