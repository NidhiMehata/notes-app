import { useEffect } from "react";
import "./Toast.css";

type ToastProps = {
  message: string;
  onClose: () => void;
  custom_timeout?: number;
};

function Toast({ message, onClose, custom_timeout = 2000 }: ToastProps) {
  useEffect(() => {
    if (!message) {
      return;
    }

    const timeout = setTimeout(() => {
      onClose();
    }, custom_timeout);

    return () => clearTimeout(timeout);
  }, [message, onClose]);

  if (!message) {
    return null;
  }

  return <div className="toast">{message}</div>;
}

export default Toast;
