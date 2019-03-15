#include "../../src/sstscit.hpp"

#include <sst/core/component.h>
#include <sst/core/elementinfo.h>
#include <sst/core/interfaces/stringEvent.h>
#include <sst/core/link.h>
#include <sst/core/sst_config.h>

class fib_lfsr : public SST::Component {

public:

    fib_lfsr(SST::ComponentId_t, SST::Params &);

    void setup() override;

    void finish() override;

    bool tick(SST::Cycle_t);

    void handle_event(SST::Event *);

    // Register the component
    SST_ELI_REGISTER_COMPONENT(
        fib_lfsr, // class
        "proto", // element library
        "fib_lfsr", // component
        SST_ELI_ELEMENT_VERSION(1, 0, 0),
        "Simple 4-bit Fibonacci Linear Feedback Shift Register",
        COMPONENT_CATEGORY_UNCATEGORIZED
    )

    // Port name, description, event type
    SST_ELI_DOCUMENT_PORTS(
        { "fib_din", "Fibonacci LFSR reset", { "sst.Interfaces.StringEvent" }},
        { "fib_dout", "Fibonacci LFSR data_out", { "sst.Interfaces.StringEvent" }},
    )

private:

    SST::Link *m_din_link, *m_dout_link;

    // SST parameters
    SST::Output m_output;
    std::string m_clock, m_proc, m_ipc_port;

    SignalSocket m_signal_io;

};

fib_lfsr::fib_lfsr(SST::ComponentId_t id, SST::Params &params)
    : SST::Component(id), m_signal_io(socket(AF_UNIX, SOCK_STREAM, 0)),
      m_clock(params.find<std::string>("clock", "")),
      m_proc(params.find<std::string>("proc", "")),
      m_ipc_port(params.find<std::string>("ipc_port", "")),
      m_din_link(configureLink(
          "fib_din", new SST::Event::Handler<fib_lfsr>(this, &fib_lfsr::handle_event)
      )),
      m_dout_link(configureLink("fib_dout")) {

    // Initialize output
    m_output.init("\033[32mblackbox-" + getName() + "\033[0m -> ", 1, 0, SST::Output::STDOUT);

    // Just register a plain clock for this simple example
    registerClock(m_clock, new SST::Clock::Handler<fib_lfsr>(this, &fib_lfsr::tick));

    // Configure our reset
    if (!(m_din_link && m_dout_link)) {
        m_output.fatal(CALL_INFO, -1, "Failed to configure port\n");
    }

    // Tell SST to wait until we authorize it to exit
    registerAsPrimaryComponent();
    primaryComponentDoNotEndSim();

}

void fib_lfsr::setup() {

    m_output.verbose(CALL_INFO, 1, 0, "Component is being set up.\n");

    int child_pid = fork();

    if (!child_pid) {

        char *args[] = {&m_proc[0u], &m_ipc_port[0u], nullptr};
        m_output.verbose(CALL_INFO, 1, 0, "Forking process \"%s\"...\n", m_proc.c_str());
        execvp(args[0], args);

    } else {

        m_signal_io.set_addr(m_ipc_port);
        m_signal_io.recv();
        if (child_pid == m_signal_io.get<int>("pid")) {
            m_output.verbose(CALL_INFO, 1, 0, "Process \"%s\" successfully synchronized\n",
                             m_proc.c_str());
        }

    }

}

void fib_lfsr::finish() {

    m_output.verbose(CALL_INFO, 1, 0, "Destroying %s...\n", getName().c_str());

}

void fib_lfsr::handle_event(SST::Event *ev) {

    auto *se = dynamic_cast<SST::Interfaces::StringEvent *>(ev);

    if (se) {

        std::string _data_in = se->getString();
        bool keep_send = _data_in.substr(0, 1) != "0";
        bool keep_recv = _data_in.substr(1, 1) != "0";

        m_signal_io.set("reset", std::stoi(_data_in.substr(2, 1)));
        m_signal_io.set("clock", std::stoi(_data_in.substr(3, 2)));

        if (keep_send) {
            if (!keep_recv) {
                m_signal_io.set_state(false);
            } else {
                m_signal_io.set_state(true);
            }
            m_signal_io.send();
        }
        if (keep_recv) {
            m_signal_io.recv();
        }

        std::string _data_out = std::to_string(m_signal_io.get<int>("data_out"));
        m_dout_link->send(new SST::Interfaces::StringEvent(_data_out));

    }

    delete ev;

}

bool fib_lfsr::tick(SST::Cycle_t) {

    return false;

}
