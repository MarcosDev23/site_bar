document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.querySelector(".menu-toggle");
  const navLinks = document.querySelector(".nav-links");

  // Abre/Fecha menu no mobile
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("active");
  });

  // Fecha o menu ao clicar em algum link (para o scroll funcionar)
  document.querySelectorAll(".nav-links a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("active");
    });
  });
});

document.getElementById("reservaForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const nome = document.getElementById("nome").value;
  const data = document.getElementById("data_reserva").value;
  const motivo = document.getElementById("motivo").value;
  const tel_bar = "5511961699799"; // Coloque seu número aqui

  const mensagem = `Olá! Meu nome é ${nome}. Gostaria de fazer uma reserva para o dia ${data}. Motivo: ${motivo}.`;
  const url = `https://wa.me/${tel_bar}?text=${encodeURIComponent(mensagem)}`;

  window.open(url, "_blank");
});

function excluirProduto(id) {
  if (confirm("Tem certeza que deseja excluir este item?")) {
    // Redireciona para a rota de exclusão do Flask
    window.location.href = `/excluir-produto/${id}`;
  }
}

function editarProduto(id) {
  // Redireciona para a página de edição
  window.location.href = `/editar-produto/${id}`;
}

function excluirShow(id) {
  if (confirm("Deseja remover este show da agenda?")) {
    window.location.href = `/excluir-show/${id}`;
  }
}

function excluirFoto(id) {
  if (confirm("Deseja remover esta foto da galeria?")) {
    window.location.href = `/excluir-foto/${id}`;
  }
}
