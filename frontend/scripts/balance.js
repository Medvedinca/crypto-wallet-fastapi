// Функция реализующая логаут
function deleteCookie(cookieName) {
  document.cookie = cookieName + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  location.reload();
}


// Функция получения случайного числа в заданном диапозоне
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}


// Функция закрывающая окно конвертации
function closeConvert() {
  const popup = document.querySelector(".convert");
  popup.classList.remove("show");

  const input = document.querySelector(".convert-from-input");
  input.value = "";

  const select = document.querySelector(".convert-select");
  select.selectedIndex = 0;

  const button = document.querySelector(".convert-btn");
  button.classList.add("deactiv");

  const selectOptions = document.querySelectorAll(".convert-select option");
  const output = document.querySelector(".convert-to-input");
  output.value = "";

  selectOptions.forEach((option) => {
    option.hidden = false;
  });
}


// Функция закрывающая окно транзакции
function closeTrans() {
  const popup = document.querySelector(".trans");
  popup.classList.remove("show");  
}


// Функция закрывающая окно пополнения
function closeDeploy() {
  const popup = document.querySelector(".deploy");
  popup.classList.remove("show");

  const input = document.querySelector(".deploy-from-input");
  input.value = "";

  const input2 = document.querySelector(".deploy-card-number");
  input2.value = "";

  const input3 = document.querySelector(".deploy-date-number");
  input3.value = "";

  const input4 = document.querySelector(".deploy-cvv-number");
  input4.value = "";
}


// Функция закрытия окна пополнения BTC
function closeBTC() {
  const popup = document.querySelector(".deploy-btc");
  popup.classList.remove("show");
}


// Функция закрытия окна вывода BTC
function closeWithdrawBTC() {
  const popup = document.querySelector(".withdraw-btc");
  popup.classList.remove("show");

  // очистка поля ввода
  const input = document.querySelector(".withdraw-btc-from-input");
  input.value = "";

  const input2 = document.querySelector(".withdraw-btc-to-input");
  input2.value = "";
}


// Функция закрывающая окно вывода
function closeWithdraw() {
  const popup = document.querySelector(".withdraw");
  popup.classList.remove("show");

  // очистка поля ввода
  const input = document.querySelector(".withdraw-from-input");
  input.value = "";

  const input2 = document.querySelector(".withdraw-to-input");
  input2.value = "";
}


// Переменная запоминающая выделенный элемент из кошельков и истории
let selectedItem = null;


// Функция для снятия выделения
function removeActive() {
  document.querySelectorAll(".wallet, .transaction").forEach((item) => {
    item.classList.remove("active");
    closeConvert();
    closeDeploy();
    closeWithdraw();
    closeTrans();
    closeBTC();
    closeWithdrawBTC();
  });
}


// Функция добавления выделения на кошельки
function activateWallet(wallet) {
  if (selectedItem === wallet) {
    removeActive();
    selectedItem = null;
    return;
  }

  removeActive();

  wallet.classList.add("active");
  selectedItem = wallet;
}


// Функция добавления выделения на транзакции
function activateTransaction(transaction) {
  if (selectedItem === transaction) {
    removeActive();
    selectedItem = null;
    return;
  }

  removeActive();

  transaction.classList.add("active");
  selectedItem = transaction;
}


// Выделение первого элемента по умолчанию при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
  const defaultItem = document.querySelector(".wallet");
  defaultItem.classList.add("active");
  selectedItem = defaultItem;
});


// Логика реализации заблюривания балансов
document.addEventListener("DOMContentLoaded", () => {
  const switchBtn = document.querySelector(".switch-btn");
  const balance = document.querySelectorAll(".balance-result", ".wallet-value");
  const wallet = document.querySelectorAll(".wallet-value");
  const history = document.querySelectorAll(".transaction-sum");

  let blurOn = false;

  switchBtn.addEventListener("click", () => {
    switchBtn.classList.toggle("switch-on");

    blurOn = !blurOn;

    balance.forEach((elem) => {
      if (blurOn) {
        elem.classList.add("blur");
      } else {
        elem.classList.remove("blur");
      }
    });

    history.forEach((elem) => {
      if (blurOn) {
        elem.classList.add("blur");
      } else {
        elem.classList.remove("blur");
      }
    });

    wallet.forEach((elem) => {
      if (blurOn) {
        elem.classList.add("blur");
      } else {
        elem.classList.remove("blur");
      }
    });
  });
});


// Логика проверки заполнения полей и превышения максимального баланса при конвертации
document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector(".convert-from-input");
  const select = document.querySelector(".convert-select");
  const button = document.querySelector(".deactiv");

  input.addEventListener("input", check);
  select.addEventListener("change", check);

  function check() {
    let activeWallet = document.querySelector(".wallet.active");

    const amount = activeWallet.querySelector("#wallet-amount").textContent;

    if (input.value && select.value !== "start") {
      if (+input.value > +amount) {
        button.classList.add("deactiv");
      } else {
        button.classList.remove("deactiv");
      }
    } else {
      button.classList.add("deactiv");
    }
  }
});


// Логика открытия окна обмена, и получения значений в него
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".btn-exchange");
  const popup = document.querySelector(".convert");

  button.addEventListener("click", () => {
    if (document.querySelector(".wallet.active")) {
      popup.classList.add("show");

      let activeWallet = document.querySelector(".wallet.active");

      if (activeWallet) {
        let title = activeWallet.querySelector("#wallet-title").textContent;
        let currency = activeWallet.querySelector("#wallet-value-currency").textContent;
        let amount = activeWallet.querySelector("#wallet-amount").textContent;

        let selectOptions = document.querySelectorAll(".convert-select option");

        selectOptions.forEach((option) => {
          if (option.textContent === title + " " + currency) {
            option.hidden = true;
          }
        });

        document.querySelector(".convert-from-wallet").textContent = title + " " + currency;
        document.querySelector(".convert-from-currency").textContent = currency;
        document.querySelector(".convert-from-value").textContent = amount;
        document.querySelector(".from-max").textContent ="Максимальная сумма: " + amount + " " + currency;

        closeDeploy();
        closeWithdraw();
        closeTrans();
        closeBTC();
        closeWithdrawBTC();
      }
    }
  });
});


// Логика конвертации валют на лету
document.addEventListener("DOMContentLoaded", () => {
  let usd = parseFloat(document.querySelector(".usd").textContent);
  let btc = parseFloat(document.querySelector(".btc").textContent);

  const fromInput = document.querySelector(".convert-from-input");
  const toSelect = document.querySelector(".convert-select");
  const toInput = document.querySelector(".convert-to-input");

  toSelect.addEventListener("change", () => {
    toInput.value = "";
    fromInput.value = "";
  });

  const button = document.querySelector(".btn-exchange");

  button.addEventListener("click", () => {
    if (document.querySelector(".active")) {
      let activeWallet = document.querySelector(".wallet.active");

      if (activeWallet) {
        let currency = activeWallet.querySelector("#wallet-value-currency").textContent;

        if (currency === "RUB") {
          fromInput.addEventListener("input", () => {
            const amount = parseFloat(fromInput.value);

            if (toSelect.value === "usd") {
              const converted = amount / usd;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "btc") {
              const converted = amount / btc;

              toInput.value = converted.toFixed(5);
            }

            if (toSelect.value === "usdttrc20") {
              const converted = amount / usd;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usdttrc20") {
              const converted = amount / usd;

              toInput.value = converted.toFixed(2);
            }
          });
        }

        if (currency === "USD") {
          fromInput.addEventListener("input", () => {
            const amount = parseFloat(fromInput.value);

            if (toSelect.value === "rub") {
              const converted = amount * usd;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "btc") {
              const converted = amount * (usd / btc);

              toInput.value = converted.toFixed(5);
            }

            if (toSelect.value === "usdttrc20") {
              const converted = amount;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usdterc20") {
              const converted = amount;

              toInput.value = converted.toFixed(2);
            }
          });
        }

        if (currency === "BTC") {
          fromInput.addEventListener("input", () => {
            const amount = parseFloat(fromInput.value);

            if (toSelect.value === "rub") {
              const converted = amount * btc;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usd") {
              const converted = (amount * btc) / usd;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usdttrc20") {
              const converted = (amount * btc) / usd;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usdterc20") {
              const converted = (amount * btc) / usd;

              toInput.value = converted.toFixed(2);
            }
          });
        }

        if (currency === "USDTTRC20") {
          fromInput.addEventListener("input", () => {
            const amount = parseFloat(fromInput.value);

            if (toSelect.value === "rub") {
              const converted = amount * usd;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usd") {
              const converted = amount;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usdterc20") {
              const converted = amount;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "btc") {
              const converted = amount * (usd / btc);

              toInput.value = converted.toFixed(2);
            }
          });
        }

        if (currency === "USDTERC20") {
          fromInput.addEventListener("input", () => {
            const amount = parseFloat(fromInput.value);

            if (toSelect.value === "rub") {
              const converted = amount * usd;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usd") {
              const converted = amount;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "usdttrc20") {
              const converted = amount;

              toInput.value = converted.toFixed(2);
            }

            if (toSelect.value === "btc") {
              const converted = amount * (usd / btc);

              toInput.value = converted.toFixed(2);
            }
          });
        }
      }
    }
  });
});


// Логика формирования запроса обмена и отправка на сервер, приём ответа
document.addEventListener("DOMContentLoaded", () => {
  const exchange = document.querySelector(".convert-btn");

  document.addEventListener("keyup", (e) => {
    if(e.keyCode === 13) {
      const event = new Event("click");
      exchange.dispatchEvent(event);
    }  
  });

  exchange.addEventListener("click", (e) => {
    e.preventDefault();

    const input = document.querySelector(".convert-from-input").value;
    const output = document.querySelector(".convert-to-input").value;

    const inputCur = document.querySelector(".convert-from-currency").textContent;

    const select = document.querySelector(".convert-select");
    const outputCur = select.value;

    const data = {
      fromAmount: input,
      fromCurrency: inputCur,
      toAmount: output,
      toCurrency: outputCur,
    };

    fetch("/exchange", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "ok") {
          show_ok();

          location.reload();
        }
      });
  });
});


// Функция открытия системного сообщения всё окей
function show_ok() {
  const message = document.querySelector(".message-ok");

  message.classList.add("show");
}


// Функция закрытия системного сообщения всё окей
function close_ok() {
  const message = document.querySelector(".message-ok");

  message.classList.remove("show");
}


// Функция открытия системного сообщения об ошибке
function show_bad() {
  const message = document.querySelector(".message-bad");

  message.classList.add("show");
}


// Функция закрытия системного сообщения об ошибке
function close_bad() {
  const message = document.querySelector(".message-bad");

  message.classList.remove("show");
}


// Функция открытия сообщения о копировании
function show_copy() {
  const message = document.querySelector(".message-copy");

  message.classList.add("show");
}


// Функция скрытия сообщения о копировании 
function close_copy() {
  const message = document.querySelector(".message-copy");

  message.classList.remove("show");
}

// Функция показа лоадера
function open_loader() {
  const message = document.querySelector(".loader");

  message.classList.add("show");
}


// Функция скрытия лоадера
function close_loader() {
  const message = document.querySelector(".loader");

  message.classList.remove("show");
}


// Логика форматирования ввода при пополнении и проверка заполнености полей
document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector(".deploy-from-input");
  const button = document.querySelector(".deploy-btn");

  const maxLength = 16;
  const cardNumberInput = document.querySelector(".deploy-card-number");

  cardNumberInput.onkeypress = (event) => {
    if (isNaN(Number(event.key))) {
      event.preventDefault();
      return;
    }

    if (cardNumberInput.value.replace(/\D/g, "").length >= maxLength) {
      event.preventDefault();
      return;
    }

    cardNumberInput.value += event.key;
    cardNumberInput.value = cardNumberInput.value
      .replace(/\D/g, "")
      .replace(/([0-9]{4})/g, "$1 ")
      .trim();

    event.preventDefault();
  };

  const date = document.querySelector(".deploy-date-number");
  const dateLength = 5;

  date.onkeypress = (event) => {
    if (isNaN(Number(event.key))) {
      event.preventDefault();
      return;
    }

    if (date.value.length >= dateLength) {
      event.preventDefault();
      return;
    }

    if (date.value.length === 2 && event.key !== "/") {
      date.value += "/";
    }

    date.value += event.key;

    date.value = date.value
      .replace(/\D/g, "")
      .replace(/^(\d{2})(\d{0,2})/, "$1/$2");

    event.preventDefault();
  };

  input.onkeypress = (event) => {
    if (event.key.length > 1) return true;
    input.value =
      (input.value + event.key)
        .replace(/\D/g, "")
        .replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 ") + " ₽";
    event.preventDefault();
  };

  const cvv = document.querySelector(".deploy-cvv-number");
  const cvvLength = 3;

  cvv.onkeypress = (event) => {
    if (isNaN(Number(event.key))) {
      event.preventDefault();
      return;
    }

    if (cvv.value.length >= cvvLength) {
      event.preventDefault();
      return;
    }
  };
  
  function checkFilled() {
    if (
      input.value &&
      cardNumberInput.value &&
      date.value &&
      cvv.value.length == 3
    ) {
      button.classList.remove("deactiv"); // активируем
    } else {
      button.classList.add("deactiv"); // деактивируем
    }
  }

  input.oninput = checkFilled;
  cardNumberInput.oninput = checkFilled;
  date.oninput = checkFilled;
  cvv.oninput = checkFilled;
});


// Логика открытия окна пополнения для RUB и USD
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".btn-deploy");
  const deploy = document.querySelector(".deploy");

  button.addEventListener("click", () => {
    let activeWallet = document.querySelector(".wallet.active");

    if (activeWallet) {
      let currency = activeWallet.querySelector(
        "#wallet-title-currency"
      ).textContent;

      if (currency === "RUB" || currency === "USD") {
        deploy.classList.add("show");
        closeConvert();
        closeWithdraw();
        closeTrans();
        closeBTC();
        closeWithdrawBTC();
      }
    }
  });
});


// Логика форматирования полей Вывода и проверка заполнености
document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector(".withdraw-from-input");
  const button = document.querySelector(".withdraw-btn");

  const maxLength = 16;
  const cardNumberInput = document.querySelector(".withdraw-to-input");

  cardNumberInput.onkeypress = (event) => {
    if (isNaN(Number(event.key))) {
      event.preventDefault();
      return;
    }

    if (cardNumberInput.value.replace(/\D/g, "").length >= maxLength) {
      event.preventDefault();
      return;
    }

    cardNumberInput.value += event.key;
    cardNumberInput.value = cardNumberInput.value
      .replace(/\D/g, "")
      .replace(/([0-9]{4})/g, "$1 ")
      .trim();

    event.preventDefault();
  };

  input.onkeypress = (event) => {
    if (event.key.length > 1) return true;
    input.value =
      (input.value + event.key)
        .replace(/\D/g, "")
        .replace(/(\d)(?=(\d{3})+([^\d]|$))/g, "$1 ") + " ₽";
    event.preventDefault();
  };

  function checkFilled() {
    const length = cardNumberInput.value.replace(/\s/g, "").length;

    if (input.value && length >= 16) {
      button.classList.remove("deactiv"); 
    } else {
      button.classList.add("deactiv"); 
    }
  }

  input.onkeyup = checkFilled;
  cardNumberInput.onkeyup = checkFilled;
});


// Логика открытия окна вывода для RUB и USD
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".btn-withdraw");
  const withdraw = document.querySelector(".withdraw");

  button.addEventListener("click", () => {
    let activeWallet = document.querySelector(".wallet.active");

    if (activeWallet) {
      let currency = activeWallet.querySelector(
        "#wallet-title-currency"
      ).textContent;

      if (currency === "RUB" || currency === "USD") {
        withdraw.classList.add("show");
        closeConvert();
        closeDeploy();
        closeTrans();
        closeBTC();
        closeWithdrawBTC();
      }
    }
  });
});


// Логика открытия транзакции и заполнения полей в ней
document.addEventListener("DOMContentLoaded", () => {

  const trans = document.querySelectorAll('.transaction');
  const popup = document.querySelector('.trans');

  trans.forEach(tran => {

    tran.addEventListener('click', () => {
    
      if(tran.classList.contains('active')) {

        // получаем данные из transaction
        const status = tran.querySelector('.transaction-status').textContent;  
        const sum = tran.querySelector('.transaction-sum').textContent;
        const from = tran.querySelector('.transaction-from').textContent;
        const to = tran.querySelector('.transaction-to').textContent;
        const date = tran.querySelector('.transaction-date').textContent;
        const description = tran.querySelector('.transaction-description').textContent;

        // заполняем popup
        popup.querySelector('.trans-status').textContent = status; 
        popup.querySelector('.trans-sum').textContent = sum;
        popup.querySelector('.trans-from').textContent = from;
        popup.querySelector('.trans-to').textContent = to;
        popup.querySelector('.trans-date').textContent = date;
        popup.querySelector('.trans-description').textContent = description;

        popup.classList.add('show');

      } else {

        popup.classList.remove('show'); 
      
      }

    });

  });

});


// Логика отправки запроса Пополнения RUB и USD
document.addEventListener("DOMContentLoaded", () => {
  const deploy = document.querySelector(".deploy-btn");

  deploy.addEventListener("click", (e) => {
    e.preventDefault();

    const input = document.querySelector(".deploy-from-input").value;
    const card = document.querySelector(".deploy-card-number").value;

    const fromCurrency = document.querySelector(".wallet.active").querySelector('#wallet-title-currency').textContent;

    console.log(input);

    const data = {
      fromCard: card,
      fromCurrency: fromCurrency,
      sumAmount: input,
    };


    fetch("/deploy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "ok") {
          let interval = getRandomInt(5000, 15000);
          closeDeploy();
          open_loader();
          location.reload();
        }
      });
  });
});


// Логика отправки запроса Вывода RUB и USD
document.addEventListener("DOMContentLoaded", () => {
  const withdraw = document.querySelector(".withdraw-btn");

  withdraw.addEventListener("click", (e) => {
    e.preventDefault();

    const input = document.querySelector(".withdraw-from-input").value;
    const card = document.querySelector(".withdraw-to-input").value;

    const fromCurrency = document.querySelector(".wallet.active").querySelector('#wallet-title-currency').textContent;

    const data = {
      fromCard: card,
      fromCurrency: fromCurrency,
      sumAmount: input,
    };


    fetch("/withdraw", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "ok") {
          let interval = getRandomInt(5000, 15000);
          closeWithdraw();
          open_loader();
          location.reload();
        }
      });
  });
});


// Логика копирования текста по клику
document.addEventListener("DOMContentLoaded", () => {

  const div = document.querySelector('.deploy-btc-address');

  div.addEventListener('click', async () => {

    // Получаем текст элемента
    const text = div.textContent;
  
    try {
      // Записываем текст в буфер обмена
      await navigator.clipboard.writeText(text);
    } catch(err) {
      console.error('Не удалось скопировать текст: ', err);
    }
  

  show_copy();
  setTimeout(close_copy, 2000);

  });
});


// Логика открытия пополнения BTC
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".btn-deploy");
  const deploy = document.querySelector(".deploy-btc");
  const address = document.querySelector(".deploy-btc-address")
  const btc = document.querySelector(".btc-address").textContent;
  const trc = document.querySelector(".trc-address").textContent;
  const erc = document.querySelector(".erc-address").textContent;

  button.addEventListener("click", () => {
    let activeWallet = document.querySelector(".wallet.active");

    if (activeWallet) {
      let currency = activeWallet.querySelector(
        "#wallet-title-currency"
      ).textContent;

      if (currency === "BTC") {
        address.innerHTML = btc;
        deploy.classList.add("show");
        closeConvert();
        closeWithdraw();
        closeTrans();
        closeWithdrawBTC();
      };

      if (currency === "USDTTRC20") {
        address.innerHTML = trc;
        deploy.classList.add("show");
        closeConvert();
        closeWithdraw();
        closeTrans();
        closeWithdrawBTC();
      };

      if (currency === "USDTERC20") {
        address.innerHTML = erc;
        deploy.classList.add("show");
        closeConvert();
        closeWithdraw();
        closeTrans();
        closeWithdrawBTC();
      }
    }
  });
});


// Логика проверки заполнености полей вывода BTC
document.addEventListener("DOMContentLoaded", () => {

  const fromInput = document.querySelector('.withdraw-btc-from-input');
  const toInput = document.querySelector('.withdraw-btc-to-input');
  const button = document.querySelector('.withdraw-btc-btn');

  fromInput.addEventListener('input', activateButton);
  toInput.addEventListener('input', activateButton);

  function activateButton() {
  
  const maxSum = document.querySelector('.from-max-sum').innerText;

  if(fromInput.value && toInput.value && (parseFloat(fromInput.value) <= parseFloat(maxSum))) {
      button.classList.remove('deactiv'); 
  } else {
      button.classList.add('deactiv');
  }
  }

});


// Логика открытия вывода BTC
document.addEventListener("DOMContentLoaded", () => {
  const button = document.querySelector(".btn-withdraw");
  const deploy = document.querySelector(".withdraw-btc");
  const currencyTtl = document.querySelector(".crypto-currency");
  const currencyMax = document.querySelector(".from-max-currency");
  const btc = document.querySelector(".btc-max").textContent;
  const trc = document.querySelector(".trc-max").textContent;
  const erc = document.querySelector(".erc-max").textContent;
  const max = document.querySelector(".from-max-sum");

  button.addEventListener("click", () => {
    let activeWallet = document.querySelector(".wallet.active");

    if (activeWallet) {
      let currency = activeWallet.querySelector(
        "#wallet-title-currency"
      ).textContent;

      if (currency === "BTC") {
        currencyTtl.innerHTML = currency;
        currencyMax.innerHTML = currency;
        max.innerHTML = btc;
        deploy.classList.add("show");
        closeConvert();
        closeWithdraw();
        closeTrans();
        closeBTC();
      };

      if (currency === "USDTTRC20") {
        currencyTtl.innerHTML = currency;
        currencyMax.innerHTML = currency;
        max.innerHTML = trc;
        deploy.classList.add("show");
        closeConvert();
        closeWithdraw();
        closeTrans();
        closeBTC();
      };

      if (currency === "USDTERC20") {
        currencyTtl.innerHTML = currency;
        currencyMax.innerHTML = currency;
        max.innerHTML = erc;
        deploy.classList.add("show");
        closeConvert();
        closeWithdraw();
        closeTrans();
        closeBTC();
      };
    }
  });
});


// Логика отправки запроса на вывод крипты
document.addEventListener("DOMContentLoaded", () => {
  const withdrawcr = document.querySelector(".withdraw-btc-btn");

  withdrawcr.addEventListener("click", (e) => {
    e.preventDefault();

    const sum = document.querySelector(".withdraw-btc-from-input").value;
    const to_address = document.querySelector(".withdraw-btc-to-input").value;

    const currency = document.querySelector(".from-max-currency").textContent;

    let from_address;
    let from_private;

    if (currency === "BTC") {
      from_address = document.querySelector(".btc-address").textContent;
    };

    if (currency === "USDTTRC20") {
      from_address = document.querySelector(".trc-address").textContent;
    };

    if (currency === "USDTERC20") {
      from_address = document.querySelector(".erc-address").textContent;
    };

    const data = {
      from_address: from_address,
      sum: sum,
      currency: currency,
      to_address: to_address
    };

    fetch("/withdrawcrypto", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "ok") {
          let interval = getRandomInt(5000, 15000);
          closeWithdrawBTC();
          open_loader();
          location.reload();
        }
      });

  });
});