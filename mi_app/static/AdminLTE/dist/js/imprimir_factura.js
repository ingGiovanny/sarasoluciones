function generarPDFFacturaDesdeDjango(factura) {
    if (!window.jspdf || !window.jspdf.jsPDF) {
        alert("Error: La librería jsPDF no está cargada");
        return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    let yPos = 20;

    // Encabezado
    doc.setFontSize(18);
    doc.setTextColor(0, 0, 255);
    doc.text("Factura de Servicios", 105, yPos, { align: 'center' });

    yPos += 10;
    doc.setDrawColor(0);
    doc.setLineWidth(0.5);
    doc.line(20, yPos, 190, yPos);

    // Datos
    yPos += 10;
    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    doc.text(`ID Factura: ${factura.id}`, 20, yPos);

    yPos += 10;
    doc.text(`Tipo de pago: ${factura.tipo_pago}`, 20, yPos);

    yPos += 10;
    doc.text(`ID Cliente: ${factura.id_cliente}`, 20, yPos);

    yPos += 10;
    doc.text(`ID Vehículo: ${factura.id_vehiculo}`, 20, yPos);

    yPos += 10;
    doc.text(`ID Tipo Mantenimiento: ${factura.id_tipo_mantenimiento}`, 20, yPos);

    yPos += 10;
    doc.text("Servicio prestado:", 20, yPos);
    const servicioLines = doc.splitTextToSize(factura.servicio_prestado, 170);
    yPos += 10;
    doc.text(servicioLines, 20, yPos);
    yPos += (servicioLines.length * 7);

    yPos += 5;
    doc.text(`Nombre empresa: ${factura.nombre_empresa}`, 20, yPos);

    yPos += 10;
    doc.text(`Dirección empresa: ${factura.direccion_empresa}`, 20, yPos);

    yPos += 10;
    doc.text(`ID Empleado: ${factura.id_empleado}`, 20, yPos);

    // Guardar
    doc.save(`Factura_${factura.id}.pdf`);

    if (typeof mostrarMensaje === 'function') {
        mostrarMensaje("Factura generada correctamente");
    }
}
